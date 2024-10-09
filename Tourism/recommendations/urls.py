from django.urls import path
from recommendations import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('user/<int:user_id>/add_survey/', views.add_survey, name='add_survey'),
    path('explore/<int:user_id>/explore/', views.explore, name='explore'),
    path('restaurant/recommend/<str:algo_type>/', views.input_cuisine, name='input_cuisine'),
    path('restaurant/recommend/list/<str:algo_type>/', views.recommendation_list, name='recommendation_list'),
    path('restaurant/recommend/detail/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('restaurant/recommend/time/', views.timing_list, name='timing_list'),
]
