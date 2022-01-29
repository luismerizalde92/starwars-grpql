import json

from graphql_relay import to_global_id

from graphene_django.utils.testing import GraphQLTestCase

from swapi.schema import schema

from app.models import Planet, People, Film


class FirstTestCase(GraphQLTestCase):
    fixtures = ['app/fixtures/unittest.json']
    GRAPHQL_SCHEMA = schema

    def test_people_query(self):
        response = self.query(
            '''
                query{
                  allPlanets {
                    edges{
                      node{
                        id
                        name
                      }
                    }
                  }
                }
            ''',
        )
        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        self.assertEqual(len(content['data']['allPlanets']['edges']), 61)


class PeopleTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    fixtures = ['app/fixtures/unittest.json']

    def setUp(self):
        self.planet_1 = Planet.objects.create(
                                name='Jupyter')
        self.planet_1_id = to_global_id(type='Planet', id=self.planet_1.id)

        self.planet_tattoine = Planet.objects.get(
                                name='Tatooine')
        self.planet_tattoine_id = to_global_id(
            type='Planet', id=self.planet_tattoine.id)

        self.film_new_hope = Film.objects.get(title='A New Hope')
        self.film_new_hope_id = to_global_id(
            type='Film', id=self.film_new_hope.id)

        self.leia_organa = People.objects.get(name='Leia Organa')
        self.leia_organa_id = to_global_id(
            type='People', id=self.leia_organa.id)

    def test_create_no_existing_people_mutation(self):
        response = self.query(
            '''
            mutation CreatePeopleMutation(
              $input: CreatePeopleMutationInput!
              ) {
                createPeopleMutation(input: $input) {
                  people {
                    id
                    name
                 }
                }
              }
            ''',
            # op_name='createPeopleMutation',
            input_data={
                'name': 'Luis Solo',
                'homeWorld': self.planet_1_id
            }
        )

        if 'errors' in response.json():
            print(response.json()['errors'])

        # Validar que le codigo de respuesta sea 200
        self.assertResponseNoErrors(response)

        # Validar que el contenido de la respuesta sea el correcto
        self.assertDictEqual({
            "people": {
                "id": "UGVvcGxlVHlwZTo4OQ==",
                "name": "Luis Solo"}
            }, response.json()['data']['createPeopleMutation'])

    def test_create_existing_people_mutation(self):
        """
        Prueba para validar que no se puedan crear usuarios con el mismo
        nombre
        """

        response = self.query(
            '''
            mutation CreatePeopleMutation(
              $input: CreatePeopleMutationInput!
              ) {
                createPeopleMutation(input: $input) {
                  people {
                    id
                    name
                 }
                }
              }
            ''',
            input_data={
                'name': 'Darth Vader',
                'homeWorld': self.planet_tattoine_id
            }
        )

        # validar que el servidor arroje errores
        self.assertEqual('errors' in response.json(), True)

    def test_update_no_existing_people_mutation(self):
        """
        Prueba para verificar que no se pueda editar un usuario que no exista
        """
        no_existing_people_id = 'UGVvcGxlVHlwZTo5Nw=='
        response = self.query(
            '''
            mutation UpdatePeopleMutation(
              $input: UpdatePeopleMutationInput!
              ) {
                updatePeopleMutation(input: $input) {
                  people {
                    id
                    name
                    films {
                      id,
                      title
                    }
                 }
                }
              }
            ''',
            input_data={
                'id': no_existing_people_id,
                'films': [
                    self.film_new_hope_id
                ]
            }
        )

        # validar que el servidor arroje errores
        self.assertEqual('errors' in response.json(), True)

    def test_update_existing_people_mutation(self):
        """
        Prueba para verificar que un usuario existente se pueda editar y
        que si el campo films se agrega quede almacenado correctamente
        """
        response = self.query(
            '''
            mutation UpdatePeopleMutation(
              $input: UpdatePeopleMutationInput!
              ) {
                updatePeopleMutation(input: $input) {
                  people {
                    id
                    name
                    films {
                      id,
                      title
                    }
                 }
                }
              }
            ''',
            input_data={
                'id': self.leia_organa_id,
                'films': [
                    self.film_new_hope_id
                ]
            }
        )

        # Validar que le codigo de respuesta sea 200
        self.assertResponseNoErrors(response)

        # Validar que el numero de filmes del personaje sea uno
        films_count = len(
            response.json()['data']['updatePeopleMutation']['people']['films'])
        self.assertEqual(films_count, 1)
