import graphene
from graphql_relay import from_global_id
from graphql import GraphQLError

from .models import Planet, People, Film
from .types import PlanetType, PeopleType, FilmType
from .utils import generic_model_mutation_process

from django.db import transaction


class CreateUpdatePlanetMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=False)
        name = graphene.String(required=True)
        rotation_period = graphene.String(required=False)
        orbital_period = graphene.String(required=False)
        diameter = graphene.String(required=False)
        climate = graphene.String(required=False)
        gravity = graphene.String(required=False)
        terrain = graphene.String(required=False)
        surface_water = graphene.String(required=False)
        population = graphene.String(required=False)

    planet = graphene.Field(PlanetType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        raw_id = input.get('id', None)

        data = {'model': Planet, 'data': input}
        if raw_id:
            data['id'] = from_global_id(raw_id)[1]

        planet = generic_model_mutation_process(**data)
        return CreateUpdatePlanetMutation(planet=planet)


class CreatePeopleMutation(graphene.relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        height = graphene.String(required=False)
        mass = graphene.String(required=False)
        hair_color = graphene.String(required=False)
        skin_color = graphene.String(required=False)
        eye_color = graphene.String(required=False)
        birth_year = graphene.String(required=False)
        terrain = graphene.String(required=False)
        gender = graphene.String(required=False)
        home_world = graphene.String(required=True)
        films = graphene.List(graphene.String, required=False)

    people = graphene.Field(PeopleType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        raw_id = input.get('id', None)

        data = {'model': People, 'data': input}
        if raw_id:
            data['id'] = from_global_id(raw_id)[1]

        # arrojar error cuando el personaje ya esta registrado
        people_exists = People.objects.filter(name=input['name']).exists()
        if people_exists == True:
            raise GraphQLError('El personaje ya esta registrado en la base de datos')

        # obtener id planeta para conseguir el regustro en la base de datos
        planet_id = input.get('home_world', None)
        planet_id = from_global_id(planet_id)[1]
        planet = Planet.objects.get(id=planet_id)
        input['home_world'] = planet

        # obtener el id de los filmes si son enviados
        film_ids = None
        if 'films' in input:
            film_ids = input.get('films', [])
            del input['films']

        people = generic_model_mutation_process(**data)  

        # si los films existen almacenarlos en el personaje
        if film_ids:
            film_ids = [from_global_id(id)[1] for id in film_ids]
            films = Film.objects.filter(id__in=film_ids)
            for film in films:
                people.films.add(film)      
        
        return CreatePeopleMutation(people=people)



class UpdatePeopleMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.String(required=True)
        name = graphene.String(required=False)
        height = graphene.String(required=False)
        mass = graphene.String(required=False)
        hair_color = graphene.String(required=False)
        skin_color = graphene.String(required=False)
        eye_color = graphene.String(required=False)
        birth_year = graphene.String(required=False)
        terrain = graphene.String(required=False)
        gender = graphene.String(required=False)
        home_world = graphene.String(required=False)
        films = graphene.List(graphene.String, required=False)

    people = graphene.Field(PeopleType)

    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **input):
        raw_id = input.get('id', None)

        data = {'model': People, 'data': input}
        if raw_id:
            data['id'] = from_global_id(raw_id)[1]

        # obtener id planeta para conseguir el regustro en la base de datos
        if 'planet' in input:
            planet_id = input.get('home_world', None)
            planet_id = from_global_id(planet_id)[1]
            planet = Planet.objects.get(id=planet_id)
            input['home_world'] = planet

        # obtener el id de los filmes si son enviados
        film_ids = None
        if 'films' in input:
            film_ids = input.get('films', [])
            del input['films']

        people = generic_model_mutation_process(**data)  

        # si los films existen almacenarlos en el personaje
        if film_ids:
            # eliminar los filmes anetriores
            people.films.clear()

            # obtener las instancias de los filmes
            film_ids = [from_global_id(id)[1] for id in film_ids]
            films = Film.objects.filter(id__in=film_ids)

            # agregar los nuevos filmes al personale
            for film in films:
                people.films.add(film)      
        
        return UpdatePeopleMutation(people=people)
