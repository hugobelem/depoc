import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'accounts.User'

    name = factory.Faker('name')
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.django.Password('password')
    is_staff = True


class MemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'members.Member'

    name = factory.Faker('name')
    phone = '1198122222'
    email = factory.Faker('email')
