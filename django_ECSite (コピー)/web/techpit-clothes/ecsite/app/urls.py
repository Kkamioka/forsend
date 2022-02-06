from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('show/<int:pk>', views.ShowView.as_view(), name="show"),
    path('create/', views.CreateView.as_view(), name='create'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('delete/<int:pk>/', views.DeleteView.as_view(), name='delete'), 
    path('create_checkout_session/', views.create_checkout_session, name='checkout_session'),
    path('success/', views.success, name='success'),
]
