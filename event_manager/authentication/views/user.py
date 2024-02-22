from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status

from authentication.serializers import UserSerializer

class UserViewSet(APIView):
    """
    This endpoint handles the creation of any
    new user profile.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, format=None):
        password = request.data.pop("password") 
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    instance = serializer.save()
                    instance.set_password(password)
                    # Make sure that this user is a standard and does 
                    # not have access to Django Admin
                    instance.is_staff = False
                    instance.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                raise APIException(e)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)