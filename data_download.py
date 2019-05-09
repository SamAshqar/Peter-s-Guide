import requests
import json
import pprint

BASE_SEARCH_URL = 'https://api.yelp.com/v3'


def get_api_key(file):
    f = open(file, 'r')
    return f.readline().rstrip()

def get_data(url, headers, params=None):
    response = None
    try:
        response = requests.get(url=url, params=params, headers=headers)
        return response.json()
    finally:
        if response != None:
            response.close()

def _get_business_search_params():
    params = {'location': 'Irvine, CA',
            'radius': 30000,
            'categories': ['Restaurants', 'Coffee & Tea'],
            'limit': 50,
            'sort_by': 'distance',
            'offset': 0
            }
    return params
            
def _build_bussiness_search_params(api_key, params):
    business_url = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'bearer %s' % api_key}
    return business_url, headers, params

def _build_bussiness_details_params(api_key, bus_id):
    business_url = 'https://api.yelp.com/v3/businesses/{}'.format(bus_id)
    headers = {'Authorization': 'bearer %s' % api_key}
    return business_url, headers

def get_business_data():
    api_key = get_api_key('api_key.txt')
    business_url, headers, params = _build_bussiness_search_params(api_key, _get_business_search_params())
    data = get_data(business_url, headers, params)
    return data

def get_yelp_food_dict(business_data):
    api_key = get_api_key('api_key.txt')

    food_place_details = {}
    for business in business_data['businesses']:
        business_id = business['id']
        business_url, headers = _build_bussiness_details_params(api_key, business_id)
        response_details = get_data(business_url, headers)
        business_name = response_details['name']
        
        food_place_details[business_name] = {}
        
        try:
            food_place_details[business_name]['hours'] = response_details['hours']
        except KeyError:
            del food_place_details[business_name]
        else:
            food_place_details[business_name]['categories'] = response_details['categories']
            food_place_details[business_name]['coordinates'] = response_details['coordinates']
            food_place_details[business_name]['phone'] = response_details['display_phone']
            food_place_details[business_name]['image'] = response_details['image_url']
            food_place_details[business_name]['location'] = response_details['location']
            food_place_details[business_name]['rating'] = response_details['rating']
            food_place_details[business_name]['yelp_url'] = response_details['url']
    return food_place_details

def create_yelp_data_file(data):
    f = open('yelp_data.txt', 'w+')
    for business in data:
        f.write(business + '\r\n')
        for categories, val in data[business].items():
            if categories == 'coordinates':
                for coord, pos in data[business][categories].items():
                    f.write(str(coord) + '-> ' + str(pos) + '\r\n')    
            elif categories == 'location':
                addr_str = ' '.join(data[business][categories]['display_address'])
                f.write(str(categories) + '-> ' + addr_str + '\r\n') 
            else:
                f.write(str(categories) + '-> ' + str(val) + '\r\n')
    f.close()


def _convert_hours(times_dict):
    pass


if __name__ == '__main__':
    data = get_business_data()
    food_places_dict = get_yelp_food_dict(data)    
    create_yelp_data_file(food_places_dict)
    pprint.pprint(food_places_dict)

