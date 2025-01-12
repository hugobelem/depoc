import factory

from faker import Faker

from modules.contacts.models import Contacts

from django.contrib.auth import get_user_model
from django.apps import apps

User = get_user_model()
Business = apps.get_model('modules_business', 'Business')
BusinessOwner = apps.get_model('modules_business', 'BusinessOwner')


# Generate Mock Data for Model Testing
def faker(provider):
    return factory.Faker(provider=provider, locale='pt_BR')

# Generate Mock Data for API Testing
fakey = Faker(locale='pt_BR')

# Utility Class for Simplifying API Request Data
class ContactData:
    def __init__(
            self,
            name: str | Faker = None,
            code: str | Faker = None,
            entityType: str = 'PERSON',
            contactType: str = 'CUSTOMER',
            **kwargs: str,
        ):
        self.name = name if name is not None else fakey.name()
        self.code = code if code is not None else fakey.ssn()
        self.entityType = entityType
        self.contactType = contactType
        self.extra_attrs = kwargs

        for key, value in kwargs.items():
            setattr(self, key, value)

    def data(self):
        return {
            'name': self.name,
            'code': self.code,
            'entityType': self.entityType,
            'contactType': self.contactType,
            **self.extra_attrs,
        }


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    name = faker('name')
    username = faker('user_name')
    email = faker('company_email')
    password = faker('name')
    is_active = True


class OwnerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

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

    owner = factory.SubFactory(OwnerFactory)
    business = factory.SubFactory(BusinessFactory)


class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contacts

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
