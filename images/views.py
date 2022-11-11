from rest_framework.viewsets import ViewSet
from .serializers import ImageSerializer
from .models import Image
from rest_framework.response import Response
from rest_framework import status
from authentication.models import User


class ImageViewSet(ViewSet):

    def list(self, request):
        imagens = Image.objects.all()
        serializer = ImageSerializer(imagens, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        print("REQUEST...", request.data)
        try:
            user = request.data['user']
            image = request.data['image']
            name = request.data['name']
            user = User.objects.get(id=user)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        imageCreate = Image.objects.create(user=user, name=name, imagem=image)

        serializer = ImageSerializer(imageCreate)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):

        imagens = Image.objects.filter(user=pk)

        serializer = ImageSerializer(imagens, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        print("Passando pelo delete")
        print("REQUEST:....", request.data)
        try:
            id = request.data['id']
            Image.objects.filter(id=id).delete()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
