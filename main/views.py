from django.shortcuts import render
import os, requests

def home(request):
    return render(request, 'main/index.html')

def aqi_checker(request):
    aqi_data = None
    aqi_level = None

    if request.method == "POST":
        city = request.POST.get('city')
        api_key = os.getenv('OPENWEATHER_API_KEY')

        # Step 1: Get coordinates from Geocoding API
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
        geo_response = requests.get(geo_url)

        if geo_response.status_code == 200 and geo_response.json():
            location = geo_response.json()[0]
            lat = location['lat']
            lon = location['lon']

            # Step 2: Get AQI data using lat/lon
            aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
            aqi_response = requests.get(aqi_url)

            if aqi_response.status_code == 200:
                aqi_data = aqi_response.json()

                aqi_value = aqi_data['list'][0]['main']['aqi']
                AQI_LEVELS = {
                    1: "Good",
                    2: "Fair",
                    3: "Moderate",
                    4: "Poor",
                    5: "Very Poor"
                }
                aqi_level = AQI_LEVELS.get(aqi_value, "Unknown")
        else:
            aqi_data = {'error': 'City not found or invalid response from API.'}

    return render(request, 'main/aqi.html', {
        'aqi': aqi_data,
        'aqi_level': aqi_level
    }) 
from django.shortcuts import render

def aqi_levels(request):
    return render(request, 'main/aqi_levels.html')

def blogs(request):
    return render(request, 'main/blogs.html')

def about(request):
    return render(request, 'main/about.html')


import json
import cohere
import traceback
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Initialize Cohere
co = cohere.Client(settings.COHERE_API_KEY)

@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message")

            if not user_message:
                return JsonResponse({"response": "Please type something!"})

            # Use the chat API
            response = co.chat(
                message=user_message,
                model="command-r",  # You can also try "command-light"
                temperature=0.7,
                chat_history=[],
            )

            bot_message = response.text.strip()

        except Exception as e:
            traceback.print_exc()
            bot_message = "Sorry, I couldn't get a response from the AI. Please try again later."

        return JsonResponse({"response": bot_message})

    return JsonResponse({"response": "Invalid request method."}, status=405)
