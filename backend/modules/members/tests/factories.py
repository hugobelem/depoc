import factory

import ulid

from modules.members.models import Members, MembersCredentials

from django.contrib.auth import get_user_model
from django.apps import apps

User = get_user_model()
Business = apps.get_model('modules_business', 'Business')
BusinessOwner = apps.get_model('modules_business', 'BusinessOwner')


def faker(provider):
    return factory.Faker(provider=provider, locale='pt_BR')


class UserFactory(factory.django.DjangoModelFactory):
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


class CredentialsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda _: ulid.new().str)
    name = faker('name')
    username = faker('user_name')
    email = faker('company_email')
    password = faker('name')
    is_active = True


class MembersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Members

    id = factory.Sequence(lambda _: ulid.new().str)
    firstName = faker('first_name')
    lastName = faker('last_name')
    taxId = faker('cpf')
    dateOfBirth = faker('date')
    role = 'STAFF'
    status = 'ACTIVE'
    hireDate = faker('date')
    position = 'CASHIER'
    salary = '1000'
    streetAddress = faker('street_name')
    addressNumber = faker('building_number')
    neighborhood = faker('bairro')
    additionalInfo = 'complemento:'
    city = faker('city')
    state = faker('state')
    postCode = faker('postcode')
    phone = faker('phone_number')
    email = faker('company_email')
    access = True


class MembersCredentialsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MembersCredentials

    member = factory.SubFactory(MembersFactory)
    credential = factory.SubFactory(CredentialsFactory)

