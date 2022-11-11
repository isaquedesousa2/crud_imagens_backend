from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserCreateSerializer
from .models import User
from rest_framework.decorators import action
from django.contrib.auth import authenticate


class UserAuthenticationViewSet(ViewSet):

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserCreateSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request, *args, **kwargs):
        try:
            try:
                email = request.data['email']
                password = request.data['password']
            except:
                return Response({"mensagem": "Email, senha ou nome completo inválidos!"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.create_user(email=email, password=password)

                serializer = UserCreateSerializer(user)

            except:
                return Response({"mensagem": "Falha ao criar o usuário"}, status=status.HTTP_400_BAD_REQUEST)

            token = UserCreateSerializer.refreshToken(user)

        except:
            return Response({"mensagem": "Falha interna do sistema"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # serializer = UserSerializer(user, many=False)

        return Response({'user': serializer.data, 'token': token}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request, *args, **kwargs):
        print("PASSANDO PELA VIEW LOGIN")
        print("DATA LOGIN........", request.data)
        try:
            try:
                email = request.data['email']
                password = request.data['password']
            except:
                return Response({"mensagem": "Email ou senha inválidos!"}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(email=email)
            print("USER....", user)
            auth = authenticate(email=user.email, password=password)
            print("AUTH....", auth)
            if not auth:
                return Response({"mensagem": "Email ou senha incorretos!"}, status=status.HTTP_401_UNAUTHORIZED)

            token = UserCreateSerializer.refreshToken(user)
        except:
            return Response({"mensagem": "Falha interna do sistema!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = UserCreateSerializer(user)
        print("DEVOLVENDO SERIALIZER")
        return Response({'user': serializer.data, 'token': token}, status=status.HTTP_200_OK)
