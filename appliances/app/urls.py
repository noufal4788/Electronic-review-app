from django.urls import path
from . import views
from .views import review
from .views import auto_logout
from .views import product_list_by_category


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('about/', views.about, name='about'),
    path('addToCart/', views.addToCart, name='addToCart'),
    path('contact/', views.contact, name='contact'),
    path('developercontact/', views.developerContact, name='developercontact'),
    path('payment/', views.payment, name='payment'),
    
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('products/', views.product_list, name='products'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/review/', views.product_review, name='product_review'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('like-review/<int:review_id>/', views.like_review, name='like_review'),
    path('dislike-review/<int:review_id>/', views.dislike_review, name='dislike_review'),
    path('auto_logout/', auto_logout, name='auto_logout'),
    path('products/<slug:category_slug>/', product_list_by_category, name='product_list_by_category'),
   
]
   
    


