from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .restapis import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, SentimentOptions


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
# def login_request(request):
# ...

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...

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
# def add_review(request, dealer_id):
# ...

