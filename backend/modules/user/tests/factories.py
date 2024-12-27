import factory

import ulid

from django.contrib.auth import get_user_model

User = get_user_model()


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