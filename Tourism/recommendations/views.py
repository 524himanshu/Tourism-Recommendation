# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from recommendations.forms import SignUpForm, UserSurveyForm
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import UserSurvey, Restaurant
from recommendations.restaurant.forms import CuisineForm
from recommendations.restaurant.nearby import find_nearby
from recommendations.restaurant.rating_algo import find_rating
from recommendations.restaurant.price_algo import find_price
from recommendations.restaurant.user_personalized import find_personalized
from recommendations.restaurant.timing_algo import find_timing

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
















            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('add_survey', user_id=user.id)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def add_survey(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserSurveyForm(request.POST)
        if form.is_valid():
            UserSurvey.objects.create(
                user=user,
                home_delivery=form.cleaned_data['home_delivery'],
                smoking=form.cleaned_data['smoking'],
                alcohol=form.cleaned_data['alcohol'],
                wifi=form.cleaned_data['wifi'],
                valetparking=form.cleaned_data['valetparking'],
                rooftop=form.cleaned_data['rooftop']
            )
            return redirect('explore', user_id=user.id)
    else:
        form = UserSurveyForm()
    return render(request, 'add_survey.html', {'user': user, 'form': form})

def explore(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'explore.html', {'user': user})

def input_cuisine(request, algo_type):
    if algo_type == 'timing':
        return redirect(reverse('timing_list'))



    form = CuisineForm()
    return render(request, 'restaurant/input_cuisine.html', {'form': form, 'algo_type': algo_type})

def recommendation_list(request, algo_type):
    form = CuisineForm(request.POST)
    if form.is_valid():
        cuisine = form.cleaned_data['cuisine']
        nearby_rid = find_nearby()
        
        if algo_type == 'nearby':
            recommend_rid = nearby_rid
        elif algo_type == 'rating':
            recommend_rid = find_rating(nearby_rid, cuisine)
        elif algo_type == 'price':
            recommend_rid = find_price(nearby_rid, cuisine)
        elif algo_type == 'personalized':
            recommend_rid = find_personalized(nearby_rid, cuisine)

        restaurants = Restaurant.objects.filter(id__in=recommend_rid)
        restaurant_list = list(restaurants)
        
        return render(request, 'restaurant/recommendation_list.html', {'cuisine': cuisine, 'restaurant_list': restaurant_list})


    form = CuisineForm()
    return render(request, 'restaurant/input_cuisine.html', {'form': form})

def timing_list(request):
    nearby_rid = find_nearby()
    recommend_rid = find_timing(nearby_rid)

    restaurants = Restaurant.objects.filter(id__in=recommend_rid)
    restaurant_list = list(restaurants)

    return render(request, 'restaurant/timing_list.html', {'restaurant_list': restaurant_list})

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    return render(request, 'restaurant/restaurant_detail.html', {'restaurant': restaurant})
