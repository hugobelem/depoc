from rest_framework import serializers

from .models import Customer, Supplier


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'customer': {
                'id': representation.pop('id'),
                'code': representation.pop('code'),
                'name': representation.pop('name'),
                'alias': representation.pop('alias'),
                'gender': representation.pop('gender'),
                'cpf': representation.pop('cpf'),
                'is_active': representation.pop('is_active'),
                'notes': representation.pop('notes'),
                'contact': {
                    'phone': representation.pop('phone'),
                    'email': representation.pop('email'),
                },
                'address': {
                    'postcode': representation.pop('postcode'),
                    'city': representation.pop('city'),
                    'state': representation.pop('state'),
                    'address': representation.pop('address'),
                },
                'metrics': {
                    'amount_spent': representation.pop('amount_spent'),
                    'number_of_orders': representation.pop('number_of_orders'),
                },
                'metadata': {
                    'created_at': representation.pop('created_at'),
                    'updated_at': representation.pop('updated_at'),
                },
            }
        }
    

    def create(self, validated_data):
        business = self.context['business']
        
        customer = super().create(validated_data)
        customer.business = business
        customer.save()

        return customer


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'supplier': {
                'id': representation.pop('id'),
                'code': representation.pop('code'),
                'legal_name': representation.pop('legal_name'),
                'trade_name': representation.pop('trade_name'),
                'cnpj': representation.pop('cnpj'),
                'ie': representation.pop('ie'),
                'im': representation.pop('im'),
                'is_active': representation.pop('is_active'),
                'notes': representation.pop('notes'),
                'contact': {
                    'phone': representation.pop('phone'),
                    'email': representation.pop('email'),
                },
                'address': {
                    'postcode': representation.pop('postcode'),
                    'city': representation.pop('city'),
                    'state': representation.pop('state'),
                    'address': representation.pop('address'),
                },
                'metadata': {
                    'created_at': representation.pop('created_at'),
                    'updated_at': representation.pop('updated_at'),
                },
            }
        }
    

    def create(self, validated_data):
        business = self.context['business']
        
        supplier = super().create(validated_data)
        supplier.business = business
        supplier.save()

        return supplier
