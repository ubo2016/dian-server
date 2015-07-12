#! -*- encoding:utf-8 -*-
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from post.models import Tag
from post.models import Like
from post.models import Image
from post.models import Post

from post.serializers import TagSerializer
from post.serializers import LikeSerializer
from post.serializers import ImageSerializer
from post.serializers import PostSerializer


@api_view(['GET'])
def list_post(request):
    return Response("Hello list_post", status=status.HTTP_200_OK)


@api_view(['POST'])
def create_post():
    pass


@api_view(['GET'])
def get_post():
    pass


@api_view(['POST'])
def update_post():
    pass


@api_view(['GET'])
def list_tag(request):
    serializer = TagSerializer(Tag.objects.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_tag():
    pass


@api_view(['GET'])
def get_tag():
    pass


@api_view(['TAG'])
def update_tag():
    pass


@api_view(['GET'])
def list_tag_with_restaurant(request, restaurant_openid):
    serializer = TagSerializer(Tag.objects.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
