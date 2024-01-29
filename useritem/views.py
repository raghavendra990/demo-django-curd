from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import functools
# Create your views here.

from .models import Item
from userauth.models import UserModel
from .serializers import ItemListSerializer, ItemGetCreateUpdateSerializer

from userauth.log import LOGGER, raise_400

from userauth.authentication import IsTokenValid
SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
ITEM_DOES_NOT_EXIST = "Item not Exist"
class ItemListCreateAPIView(generics.ListCreateAPIView):
    """
    List study API View
    """
    permission_classes = (IsAuthenticated,  IsTokenValid)

    def get_serializer_class(self):
        
        return ItemListSerializer

    def get_queryset(self):
        res = Item.objects.filter(user=UserModel(id=self.request.user.user_id))
        return res

    def perform_create(self, serializer):
        if not serializer.is_valid():
            raise_400('Forbidden to create core Item')
        user_id = self.request.user.user_id
        user_obj = UserModel(id=self.request.user.user_id)
        name = serializer.validated_data['name']
        price = serializer.validated_data['price']
        Item.add(user_id, name, price)

class ItemRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Study Retrieve Update Delete APIView
    """
    serializer_class = ItemGetCreateUpdateSerializer
    permission_classes = (IsAuthenticated, IsTokenValid, )

    def get_queryset(self):
        user_id = self.request.user.user_id
        user_obj = UserModel(id=user_id)
        return Item.objects.filter(user=user_obj)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.user_id)

    def delete(self, request, *args, **kwargs):
        try:
            item_id = kwargs['pk']
            item_obj = Item.objects.get(id = item_id)
            item_obj.delete()
        except Exception as e:
            raise_400(ITEM_DOES_NOT_EXIST)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ItemFinalAmount(APIView):

    permission_classes = [IsAuthenticated, IsTokenValid,]
    def get_aggregated_acount(self, user_id):
        user_obj = UserModel(id=user_id)
        items = Item.objects.filter(user = user_obj)
        final_amount = functools.reduce(lambda a,b:a +b ,  [ item.price for item in items  ])
        return final_amount
    
    def get(self, request):
        user_id = request.user.user_id
        final_amount = self.get_aggregated_acount(user_id)
        return Response(status=200, data={"amount": final_amount})