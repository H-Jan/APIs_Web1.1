import os
import requests

from pprint import PrettyPrinter
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file
from geopy.geocoders import Nominatim


################################################################################
## SETUP
################################################################################

app = Flask(__name__)

# Get the API key from the '.env' file
load_dotenv()

pp = PrettyPrinter(indent=4)

API_KEY = os.getenv('API_KEY')
API_URL = 'http://api.openweathermap.org/data/2.5/weather'


################################################################################
## ROUTES
################################################################################

@app.route('/')
def home():
    """Displays the homepage with forms for current or historical data."""
    context = {
        'min_date': (datetime.now() - timedelta(days=5)),
        'max_date': datetime.now()
    }
    return render_template('home.html', **context)

def get_letter_for_units(units):
    """Returns a shorthand letter for the given units."""
    return 'F' if units == 'imperial' else 'C' if units == 'metric' else 'K'

@app.route('/results')
def results():
    """Displays results for current weather conditions."""
    # TODO: Use 'request.args' to retrieve the city & units from the query
    # parameters.
    city = request.args.get('city')
    units = request.args.get('units')

    params = {
        "appid": API_KEY,
        #I am assuming that I should not put my actual API key 

        "q": city,
        "units": units
        # See the documentation here: https://openweathermap.org/current

    }

    result_json = requests.get(API_URL, params=params).json()

    # Uncomment the line below to see the results of the API call!
    pp.pprint(result_json)

    # For the sunrise & sunset variables, I would recommend to turn them into
    # datetime objects. You can do so using the `datetime.fromtimestamp()` 
    # function.
    context = {
        'date': datetime.now(),
        'city': city,
        'description': result_json['weather'][0]['description'],
        'temp': result_json['main']['temp'],
        'humidity': result_json['main']['humidity'],
        'wind_speed': result_json['wind']['speed'],
        'sunrise': datetime.fromtimestamp(result_json['sys']['sunrise']),
        'sunset': datetime.fromtimestamp(result_json['sys']['sunset']),
        'units_letter': get_letter_for_units(units)
    }

    return render_template('results.html', **context)


@app.route('/comparison_results')
def comparison_results():
    """Displays the relative weather for 2 different cities."""
    # TODO: Use 'request.args' to retrieve the cities & units from the query
    # parameters.
    city1 = request.args.get('city1')
    city2 = request.args.get('city2')
    units = request.args.get('city3')

    def helper_function(city):
        diction = {
            'appid': API_KEY,
            'q': city,
            'units': units
        }

        return request.get(API_URL, diction=diction).json()

    city1_call_info = helper_function(city1)
    city2_call_info = helper_function(city2)


    context = {
        'date'L datetime.now(),
        'units_info': get_letter_for_units(units),
        'city1_stats': 
            {
                'city': city1_call_info['name'],
                'temp': city1_call_info['main']['temp'],
                'humidity': city1_call_info['main']['humidity'],
                'wind_speed': city1_call_info['wind']['speed'],
                'sunrise': datetime.fromtimestamp(city1_call_info['sys']['sunrise']),
                'sunset': datetime.fromtimestamp(city1_call_info['sys']['sunset']),
            },
        'city2_stats':
            {
                'city': city2_call_info['name'],
                'temp': city2_call_info['main']['temp'],
                'humidity': city2_call_info['main']['humidity'],
                'wind_speed': city2_call_info['wind']['speed'],
                'sunrise': datetime.fromtimestamp(city2_call_info['sys']['sunrise']),
                'sunset': datetime.fromtimestamp(city2_call_info['sys']['sunset']),
             }

        }


    return render_template('comparison_results.html', **context)


if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
