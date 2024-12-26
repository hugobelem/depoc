import factory

import ulid

from modules.contacts.models import Contacts


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contacts

    id = factory.Sequence(lambda _: ulid.new().str)
    name = factory.Faker('name')
    code = factory.Sequence(lambda n: f'{n + 1}')
    entityType = 'PERSON'
    contactType = 'CUSTOMER'
    ''' Optional fields:
        alias = ''
        entityId = ''
        taxPayer = ''
        companyTaxCategory = ''
        stateRegistration = ''
        cityRegistration = ''
        postCode = ''
        city = ''
        state = ''
        streetAddress = ''
        addressNumber = ''
        neighborhood = ''
        additionalInfo = ''
        phone = ''
        email = ''
        dateOfBirth = ''
        gender = ''
        maritalStatus = ''
        notes = ''
        status = ''
        created = ''    
    '''
    
