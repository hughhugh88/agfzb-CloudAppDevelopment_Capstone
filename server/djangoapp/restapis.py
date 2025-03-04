import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, SentimentOptions



# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print('GET from {}'.format(url))
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
    except:
        print('Network exception occurred')
    status_code = response.status_code
    print('With status {} '.format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    print(kwargs)
    print('POST to {} '.format(url))
    payload = json.dumps(payload)
    print(payload)
    response = requests.post(url, params=kwargs, json=payload)
    status_code = response.status_code
    print('With status {} '.format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    id = kwargs.get('id')
    # state = kwargs.get('state')
    json_result = get_request(url)

    if json_result:
        dealers = json_result
        for dealer in dealers:
            dealer_doc = dealer['doc']
            if id:
                if dealer_doc['id'] ==id:
                    dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                        id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                        short_name=dealer_doc["short_name"],
                                        st=dealer_doc["st"], zip=dealer_doc["zip"])
                    results=dealer_obj

            else:
                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],
                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
                results.append(dealer_obj)
        
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get('id')
    json_result = get_request(url)

    if json_result:
        reviews = json_result
        for review in reviews:
            dealer_review = review['doc']
            if dealer_review['dealership'] == id:
                review_obj = DealerReview(dealership = dealer_review['dealership'],
                                        name = dealer_review['name'],
                                        purchase= dealer_review['purchase'],
                                        review = dealer_review['review']
                                        )
                if 'id' in dealer_review:
                    review_obj.id = dealer_review['id']
                if 'purchase_date' in dealer_review:
                    review_obj.purchase_date = dealer_review['purchase_date']
                if 'car_make' in dealer_review:
                    review_obj.car_make = dealer_review['car_make']
                if 'car_model' in dealer_review:
                    review_obj.car_model = dealer_review['car_model']
                if 'car_year' in dealer_review:
                    review_obj.car_year = dealer_review['car_year']
                
                sentiment = analyze_review_sentiments(review_obj.review)
                print(sentiment)
                review_obj.sentiment = sentiment
                results.append(review_obj)
        
        return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    url = 'https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/76c7f3b6-5a0f-4523-8e6e-dfc4204827ba'
    api_key = 'Srl4vAlNZt2AuOrvyvzu5PpETzFx577dLlvcv8S_Ucu6'
    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1(version = '2021-08-01',
                                         authenticator = authenticator)
    nlu.set_service_url(url)
    response = nlu.analyze(text = text, features = Features(sentiment=SentimentOptions(targets=[text]))).get_result()
    # print(json.dumps(response, indent = 2))
    label = response['sentiment']['document']['label']

    return label



