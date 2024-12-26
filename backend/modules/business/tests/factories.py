import factory

import ulid

from modules.business.models import (Business, BusinessOwner)

from django.contrib.auth import get_user_model

User = get_user_model()

def faker(provider):
    return factory.Faker(provider=provider, locale='pt_BR')


class MemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda _: ulid.new().str)
    name = faker('name')
    username = faker('user_name')
    email = faker('company_email')
    password = faker('name')
    is_active = True


class OwnerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda _: ulid.new().str)
    name = faker('name')
    username = faker('user_name')
    email = faker('company_email')
    password = faker('name')
    is_superuser = True
    is_staff = True
    is_active = True


class BusinessFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Business

    id = factory.Sequence(lambda _: ulid.new().str)
    tradeName = faker('catch_phrase_noun')
    legalName = faker('company')
    companyType = faker('company_suffix')
    registrationNumber = faker('cnpj')
    stateRegistration = faker('ssn')
    cityRegistration = faker('ssn')
    streetAddress = faker('street_name')
    addressNumber = faker('building_number')
    neighborhood = faker('bairro')
    additionalInfo = 'complemento:'
    city = faker('city')
    state = faker('state')
    postCode = faker('postcode')
    phone = faker('phone_number')
    email = faker('company_email')
    category = ''
    active = True


class BusinessOwnerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BusinessOwner

    id = factory.Sequence(lambda _: ulid.new().str)
    owner = factory.SubFactory(OwnerFactory)
    business = factory.SubFactory(BusinessFactory)

