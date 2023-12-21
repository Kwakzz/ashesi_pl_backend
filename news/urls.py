from django.urls import path
from news.views import create_news_item, update_news_item, delete_news_item, get_news_items, get_news_item, create_news_item_tag


urlpatterns = [
    path('news-item/create/', create_news_item, name='create_news_item'),
    path('news-item/update/<int:id>/', update_news_item, name='update_news_item'),
    path('news-item/delete/<int:id>/', delete_news_item, name='delete_news_item'),
    path('news-item/get/', get_news_items, name='get_news_items'),
    path('news-item/get', get_news_item, name='get_news_item'),
    
    path('news-item-tag/create/', create_news_item_tag, name='create_news_item_tag'),
]