from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from django.contrib.auth import get_user_model

from .serializers import UserSerializer

User = get_user_model()


class GetMe(APIView):
    """
    View to get logged in user info.

    * Requires token authentication.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return information of logged in user.
        """
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, format=None):
        """
        Update information of logged in user.
        """        
        data = request.data
        default_attrs = ['name', 'email', 'username']
        data_attrs = [field for field in data.keys()]
        matching_attrs = all(item in default_attrs for item in data_attrs)

        if not data_attrs:
            return Response(f'attributes can not be empty')
        elif matching_attrs:
            user = User.objects.filter(id=request.user.id)
            update = {key: value for key, value in data.items()}
            user.update(**update)
            return Response('Ok')
        else:
            wrong_attrs = [item for item in data_attrs if item not in default_attrs]
            return Response(f'no matching attributes: {wrong_attrs}')         