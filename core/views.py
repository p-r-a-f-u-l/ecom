import random
import string

from django.contrib.auth import get_user_model, logout
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from core.serializers import RegisterSerializer
from ecom.settings import EMAIL_HOST_USER

User = get_user_model()


class UserIndex(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


def get_random_string(length=12):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    return password


@api_view(['POST', "GET"])
@authentication_classes([])
@permission_classes([])
def forgetpassword(request):
    if request.method == 'POST':
        email = request.data['email'].replace(" ", "")
        status = User.objects.filter(email=email).exists()
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            new_password = get_random_string()
            user.set_password(new_password)
            user.save()
            subject = 'Password Reset'
            msg = f'Password is reset & new password is {new_password}'
            send_to = email
            send_mail(subject, msg, EMAIL_HOST_USER,
                      [send_to], fail_silently=False)
            return Response({'exists': status, 'message': 'Password Changed.'})
        return Response({'exists': status, 'message': 'Email Not Found'})
    return Response({"email": "demo.py@example.com"})


class Logout(APIView):
    def post(self, request):
        data = self.request.data["refresh"]
        token = RefreshToken(data)
        token.blacklist()
        print(self.request.data)
        logout(request)
        return Response("LOGOUT", status=status.HTTP_200_OK)

# {
#     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1MTczMjIwMywiaWF0IjoxNjUxMTI3NDAzLCJqdGkiOiJmYThiYjFkZTViOTc0MmMzOGRmOGRlOGU5NDhjZTA0OSIsInVzZXJfaWQiOjJ9.ky6C9VJzwE81ATiYhrJ0WcvagC_pSSfXtJ0doW-Q1To",
#     "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUxNTU5NDAzLCJpYXQiOjE2NTExMjc0MDMsImp0aSI6ImZiNTI1YzVlZWY5NzQ1MjliNGNkZDMyMmQ1YjE1ZjAyIiwidXNlcl9pZCI6Mn0.LHZInZYXmChEOk3b-oXH87ghdLSiMLTjhRQu7EzsUWE"
# }
