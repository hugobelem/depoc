from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from . import services
from .throttling import BurstRateThrottle, SustainedRateThrottle
from .serializers import ContactsSerializer


class ContactsEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def post(self, request):
        business = services.get_business(request)
        if isinstance(business, Response):
            error_response = business
            return error_response
        
        data = services.get_data(request)
        if isinstance(data, Response):
            error_response = data
            return error_response

        field_errors = services.check_field_errors(request)
        if isinstance(field_errors, Response):
            error_response = field_errors
            return error_response
        
        serializer = ContactsSerializer(data=data, context={'business': business})
        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )   
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED) 


    def get(self, request, id=None):
        business = services.get_business(request)
        if isinstance(business, Response):
            error_response = business
            return error_response

        business_contacts = services.get_business_contacts(business)
        if isinstance(business_contacts, Response):
            error_response = business_contacts
            return error_response
        
        if id:
            contacts = business_contacts.filter(contact__id=id).first()
            if not contacts:
                message = 'Contact not found.'
                return Response({'error':message}, status=status.HTTP_404_NOT_FOUND)
            serializer = ContactsSerializer(contacts.contact)
        else:
            contacts = [bc.contact for bc in business_contacts]
            serializer = ContactsSerializer(contacts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
