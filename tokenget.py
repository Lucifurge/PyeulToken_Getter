import requests
import hashlib
import uuid
import random
import string

def random_string(length):
    characters = string.ascii_lowercase + "0123456789"
    return ''.join(random.choice(characters) for _ in range(length))

def encode_sig(data):
    sorted_data = {k: data[k] for k in sorted(data)}
    data_str = ''.join(f"{key}={value}" for key, value in sorted_data.items())
    return hashlib.md5((data_str + '62f8ce9f74b12f84c123cc23437a4a32').encode()).hexdigest()

def convert_token(token):
    response = requests.get(f'https://api.facebook.com/method/auth.getSessionforApp?format=json&access_token={token}&new_app_id=275254692598279')
    return response.json().get('access_token') if 'error' not in response.json() else None

def make_request(email, password, twofactor_code=None):
    device_id = str(uuid.uuid4())
    adid = str(uuid.uuid4())
    random_str = random_string(24)
    
    form = {
        'adid': adid,
        'email': email,
        'password': password,
        'format': 'json',
        'device_id': device_id,
        'cpl': 'true',
        'family_device_id': device_id,
        'locale': 'en_US',
        'client_country_code': 'US',
        'credentials_type': 'device_based_login_password',
        'generate_session_cookies': '1',
        'generate_analytics_claim': '1',
        'generate_machine_id': '1',
        'source': 'login',
        'machine_id': random_str,
        'api_key': '882a8490361da98702bf97a021ddc14d',
        'access_token': '350685531728%7C62f8ce9f74b12f84c123cc23437a4a32',
    }
    
    form['sig'] = encode_sig(form)
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    
    url = 'https://b-graph.facebook.com/auth/login'
    try:
        response = requests.post(url, data=form, headers=headers)
        data = response.json()
        
        if response.status_code == 200 and 'access_token' in data:
            print("Access Token:", data['access_token'])
        else:
            print("Login failed!")
    except Exception as e:
        print("Error:", str(e))

if __name__ == '__main__':
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    twofactor_code = input("Enter your 2-factor authentication code (or press Enter to skip): ")
    make_request(email, password, twofactor_code if twofactor_code else None)
