from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django import forms
from .models import *
from .restapis import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)
    


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        
# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print('Log out the user "{}"'.format(request.user.username))
    logout(request)
    
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.methon == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        password_confirm = request.POST['psd_confirm']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error('Please enter new username')
        if password_confirm != password:
            raise forms.ValidationError('Password do not match')
        if not user_exist:
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            user.is_superuser = False
            user.is_staff = True
            user.save()
            login(request, user)
            return redirect('djangoapp:index')
        else:
            messages.warning(request, 'The user already exists.')
            return redirect('djangoapp:registration')


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = 'https://eu-de.functions.appdomain.cloud/api/v1/web/0581ed39-c804-41c0-8c7d-094e5cc8836f/dealership-package/get-dealership'
        dealerships = get_dealers_from_cf(url)
        context['dealership_list'] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, id):
    if request.method == 'GET':
        context = {}
        dealer_url = 'https://eu-de.functions.appdomain.cloud/api/v1/web/0581ed39-c804-41c0-8c7d-094e5cc8836f/dealership-package/get-dealership'
        dealer = get_dealers_from_cf(dealer_url, id = id)
        context['dealer'] = dealer

        review_url = 'https://eu-de.functions.appdomain.cloud/api/v1/web/0581ed39-c804-41c0-8c7d-094e5cc8836f/dealership-package/get-reviews'
        reviews = get_dealer_reviews_from_cf(review_url, id = id)
        print(reviews)
        context['reviews'] = reviews

        return render(request, 'djangoapp/dealer_details.html', context)



# Create a `add_review` view to submit a review
def add_review(request, id):
    context = {}
    dealer_url = 'https://eu-de.functions.appdomain.cloud/api/v1/web/0581ed39-c804-41c0-8c7d-094e5cc8836f/dealership-package/get-dealership'
    dealer = get_dealers_from_cf(dealer_url, id = id)
    context['dealer'] = dealer
    if request.method == 'GET':
        cars = CarModel.objects.all()
        context['cars'] = cars

        return render(request, 'djangoapp/add_review.html', context)
    
    elif request.method == 'POST':
        # if request.user.is_authenticated:
        username = 'b'
        review = {}
        # car_id = request.POST['car']
        # car = CarModel.objects.get(pk=car_id)
        review['time'] = datetime.utcnow().isoformat()
        review['name'] = username
        review['dealersip'] = id
        review['review'] = request.POST['content']
        review['purchase'] = False
        if request.POST.get('purchasecheck'):
            review['purchase'] = True
        review['purchase_date'] = request.POST['purchasedate']
        # review['car_model'] = car.name
        review_post_url = 'https://eu-de.functions.appdomain.cloud/api/v1/web/0581ed39-c804-41c0-8c7d-094e5cc8836f/dealership-package/post-review'

        post_request(review_post_url, review, id = id)
        
        return redirect('djangoapp:dealer_details', id=id)
