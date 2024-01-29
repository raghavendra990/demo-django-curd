from django.conf.urls import include
from django.urls import path

from .views import ItemListCreateAPIView, ItemRetrieveUpdateDeleteAPIView, ItemFinalAmount

item_enpoints = [
        path('getorcreate',
        ItemListCreateAPIView.as_view(),
        name='Item_list_create'),
        path('<uuid:pk>',
         ItemRetrieveUpdateDeleteAPIView.as_view(),
         name='item_update_delete'),
        path('get_final_amount',
             ItemFinalAmount.as_view(),
             name="item_dinal_amount"
             )

]

urlpatterns = [
    path('item/', include(item_enpoints))
]