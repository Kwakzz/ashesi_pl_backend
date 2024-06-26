from django.urls import path
from transfer.views import create_transfer, get_transfers

urlpatterns = [
    path('player/transfer/create/', create_transfer, name='create_transfer'),
    path('player/transfer/get/', get_transfers, name='get_transfers'),   
]