from rest_framework import generics
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Item
from .serializers import ItemSerializer, UserSerializer
from django_redis import get_redis_connection
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.views import APIView
import json
import logging

logger = logging.getLogger('api')

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        redis_conn = get_redis_connection("default")
        item_cache = redis_conn.get(f'item_{pk}')

        if item_cache:
            item_cache = item_cache.decode('utf-8')
            item_cache = json.loads(item_cache)
            if not Item.objects.filter(pk=pk).exists():
                redis_conn.delete(f'item_{pk}')  # Clear stale cache
                return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
            logger.info(f'Retrieved item {pk} from cache')
            return Response(item_cache, status=status.HTTP_200_OK)
    

        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item)
        redis_conn.set(f'item_{pk}', json.dumps(serializer.data))
        logger.info(f'Fetched item {pk} from database and cached it')
        return Response(serializer.data)

    def update(self, request, pk=None, partial=False):
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            redis_conn = get_redis_connection("default")
            redis_conn.set(f'item_{pk}', json.dumps(serializer.data))
            logger.info(f'Updated item {pk} successfully')
            return Response(serializer.data)
        
        logger.warning(f'Failed to update item {pk}: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        item = get_object_or_404(Item, pk=pk)
        item.delete()
        redis_conn = get_redis_connection("default")
        redis_conn.delete(f'item_{pk}')
        
        logger.info(f'Successfully deleted item with id: {pk}')
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"User {serializer.data['username']} registered successfully")
            return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        
        logger.error(f"User registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)