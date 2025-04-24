from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import MemberSerializer

from shared import (
    error,
    validate,
    paginate,
    IsOwner,
    BurstRateThrottle,
    SustainedRateThrottle,
    get_user_business,
)


class MemberEndpoint(APIView):
    permission_classes = [IsOwner]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get(self, request, member_id=None):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        members = business.members

        if member_id:
            member = members.filter(id=member_id).first()
            
            if not member:
                error_response = error.builder(404, 'Member not found.')
                return Response(error_response, status.HTTP_404_NOT_FOUND)
            
            serializer = MemberSerializer(member)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            serializer = MemberSerializer(members, many=True)
            paginated_data = paginate(serializer.data, request, 50)
            return paginated_data


    def post(self, request):
        data = request.data
        post_data = data.copy()

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        invalid_params = validate.params(request, MemberSerializer)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        post_data['business'] = business.id
        serializer = MemberSerializer(data=post_data)

        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


    def patch(self, request, member_id):
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        invalid_params = validate.params(request, MemberSerializer)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        members = business.members
        member = members.filter(id=member_id).first()
        if not member:
            error_response = error.builder(404, 'Member not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)

        serializer = MemberSerializer(instance=member, data=data, partial=True)

        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


    def delete(self, request, member_id):
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        members = business.members
        member = members.filter(id=member_id).first()
        if not member:
            error_response = error.builder(404, 'Member not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        member.is_active = False
        member.save()
        credential = member.credential
        credential.is_active = False
        credential.save()
        
        data = {
            'transaction': {
                'id': member.id,
                'is_active': False,
            }
        }

        return Response(data, status.HTTP_200_OK)
