from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('simplelamps/', views.LampList.as_view(), name='simplelamp_list'),
    # path('simplelamps/', views.simplelamp_list, name='simplelamp_list'),
    # path('simplelamps/<int:lamp_id>/', views.simplelamp_details, name='simplelamp_detail'),
    path('simplelamps/<int:pk>/', views.LampDetails.as_view(), name='simplelamp_detail'),
    path('simplelamps/create/', views.LampCreateView.as_view(), name='simplelamp_create'),
    path('book-ticket/<int:pk>/', views.book_ticket, name='book_ticket'),
]
