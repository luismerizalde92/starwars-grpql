import graphene
from graphene_django.filter import DjangoFilterConnectionField

from .mutations import (
    CreateUpdatePlanetMutation,
    CreatePeopleMutation,
    UpdatePeopleMutation
)
from .types import PlanetType, PeopleType, FilmType, DirectorType, ProducerType


class Query(graphene.ObjectType):
    planet = graphene.relay.Node.Field(PlanetType)
    all_planets = DjangoFilterConnectionField(PlanetType)

    people = graphene.relay.Node.Field(PeopleType)
    all_people = DjangoFilterConnectionField(PeopleType)

    film = graphene.relay.Node.Field(FilmType)
    all_films = DjangoFilterConnectionField(FilmType)

    director = graphene.relay.Node.Field(DirectorType)
    all_directors = DjangoFilterConnectionField(DirectorType)

    producer = graphene.relay.Node.Field(ProducerType)
    all_producers = DjangoFilterConnectionField(ProducerType)


class Mutation(graphene.ObjectType):
    create_update_planet_mutation = CreateUpdatePlanetMutation.Field()
    create_people_mutation = CreatePeopleMutation.Field()
    update_people_mutation = UpdatePeopleMutation.Field()
