import factory

import ulid

from modules.members.models import Members, MembersCredentials

from django.contrib.auth import get_user_model

User = get_user_model()


def faker(provider):
    return factory.Faker(provider=provider, locale='pt_BR')


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