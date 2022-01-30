import graphene
from graphene_django.types import DjangoObjectType

from .models import Planet, People, Film, Director, Producer


class PlanetType(DjangoObjectType):
    class Meta:
        model = Planet
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            'name': ['iexact', 'icontains', 'contains', 'exact'], }


class DirectorType(DjangoObjectType):
    class Meta:
        model = Director
        interfaces = (graphene.relay.Node,)
        filter_fields = ['name']


class ProducerType(DjangoObjectType):
    class Meta:
        model = Producer
        interfaces = (graphene.relay.Node,)
        filter_fields = ['name']


class Episode(graphene.Enum):
    EPISODE_IV = '4'
    EPISODE_V = '5'
    EPISODE_VI = '6'
    EPISODE_I = '1'
    EPISODE_II = '2'
    EPISODE_III = '3'


class FilmType(DjangoObjectType):
    # TODO: Agregar choices para el episode_id
    episode_id = Episode()

    class Meta:
        model = Film
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            'title': ['iexact', 'icontains', 'contains', 'exact'],
            'episode_id': ['exact'],
            'release_date': ['exact']
        }


class Gender(graphene.Enum):
    MALE = 'male'
    FEMALE = 'female'
    HERMAPHRODITE = 'hermaphrodite'
    NA = 'n/a'


class PeopleType(DjangoObjectType):
    #gender = graphene.Enum('PeopleGenderEnum', People.GENDER)
    gender = Gender()
    films = graphene.List(FilmType)

    class Meta:
        model = People
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            'name': ['iexact', 'icontains', 'contains', 'exact'],
            'gender': ['exact']
        }
        convert_choices_to_enum = False

    def resolve_films(root, info, **kwargs):
        # Querying a list
        people = People.objects.get(name=root)
        print(people.films.all())
        return people.films.all()
