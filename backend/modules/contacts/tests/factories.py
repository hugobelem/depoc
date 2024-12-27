import factory

import ulid

from modules.contacts.models import Contacts

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


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contacts

    id = factory.Sequence(lambda _: ulid.new().str)
    name = faker('name')
    code = factory.Sequence(lambda n: f'{n + 1}')
    entityType = 'PERSON'
    contactType = 'CUSTOMER'
    alias = faker('first_name')
    entityId = faker('cpf')
    streetAddress = faker('street_name')
    addressNumber = faker('building_number')
    neighborhood = faker('bairro')
    additionalInfo = 'complemento:'
    city = faker('city')
    state = faker('state')
    postCode = faker('postcode')
    phone = faker('phone_number')
    email = faker('ascii_free_email')
    dateOfBirth = faker('date')
    gender = 'MALE'
    maritalStatus = 'SINGLE'
    notes = 'Customer is a faker'
    status = 'ACTIVE'


class SupplierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contacts

    id = factory.Sequence(lambda _: ulid.new().str)
    name = faker('company')
    code = factory.Sequence(lambda n: f'{n + 1}')
    entityType = 'BUSINESS'
    contactType = 'SUPPLIER'
    alias = faker('catch_phrase_noun')
    entityId = faker('cnpj')
    taxPayer = 'CONTRIBUINTE'
    companyTaxCategory = faker('company_suffix')
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
    dateOfBirth = faker('date')
    status = 'ACTIVE'