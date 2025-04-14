import requests

def geo(ip):
    global country, countrycode, city, zip, lat, lon, timezone, region_name
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        data = response.json()
        country, countrycode, city, zip, lat, lon, timezone, reigon_name = (
            data['country'], data['countryCode'], data['city'],
            data['zip'], data['lat'], data['lon'],
            data['timezone'], data['reigonName']
        )
    except:
        try:
            response = requests.get(f'https://ipapi.co/{ip}/json/')
            data = response.json()
            country, countrycode, city, zip, lat, lon, timezone, region_name = (
                data['country_name'], data['country_code'], data['city'],
                data['postal'], data['latitude'], data['longitude'],
                data['timezone'], data['region']
            )
        except Exception as e:
            print(f'[iplo] Error fetching geolocation. Error: {e}')