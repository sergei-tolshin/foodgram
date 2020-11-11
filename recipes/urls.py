from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('recipe/new/', views.new_recipe, name='new_recipe'),
    path('recipe/<slug:slug>-<int:recipe_id>/',
         views.view_recipe, name='recipe'),
    path('recipe/<slug:slug>-<int:recipe_id>/edit/',
         views.edit_recipe, name='edit_recipe'),
    path('recipe/<slug:slug>-<int:recipe_id>/delete/',
         views.delete_recipe, name='delete_recipe'),

    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('favorites/', views.favorites, name='favorites'),
    path('purchases/', views.purchases, name='purchases'),
    path('purchases/download/', views.purchases_to_pdf, name='download'),
    path('<username>/', views.profile, name='profile'),
]
