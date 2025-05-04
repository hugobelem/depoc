import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'accounts.User'

    name = factory.Faker('name')
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.django.Password('password')
    is_staff = True


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'contacts.Customer'

    name = factory.Faker('name')


class SupplierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'contacts.Supplier'

    legal_name = factory.Faker('name')


class PayableFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'billing.Payment'

    payment_type = 'payable'
    issued_at = '2025-01-01'
    due_at = '2025-01-01'
    total_amount = 100
