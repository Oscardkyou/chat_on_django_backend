from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView, name='index'),
    path('chat/', views.chat_view, name='chats'),
    path('chat/<int:sender>/<int:receiver>/', views.message_view, 
         name='chat'),
    path('api/messages/<int:sender>/<int:receiver>/', views.message_list,
         name='message-detail'),
    path('api/messages/', views.message_list, name='message-list'),
    path('logout/', views.LogoutView, name='logout'),
    path('register/', views.register_view, name='register'),
]