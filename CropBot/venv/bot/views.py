from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse, Body, Message, Redirect 

from .query_weather import get_weather, generate_weather_params,model_predict
from django.conf import settings

@csrf_exempt
def webhook(request):
    response = MessagingResponse()
    if request.method == "POST":
        lat, lon = request.POST.get('Latitude'), request.POST.get('Longitude')
        params = request.POST.get('Body')
        if lat and lon:
            weather_response = get_weather(lat, lon, 'd0a2301b1066be60a90b946462380bab')
            weather_params = generate_weather_params(weather_response)
            request.session['temp']= weather_params["temperature"]
            request.session['humid']=weather_params["humidity"]
            message_body1 = f" *Great! We got your co-ordinates.* \n\n"\
                        f"{weather_params['location']}, {weather_params['description']}, \n" \
                        f"Temperature: {weather_params['temperature']}.\n"\
                        f"Humidity: {weather_params['humidity']}.\n"\
            
            message_body2 = f"Now please tell us about your *Soil Quality* in following parameter formats:\n\n"\
                        f"1. Nitrogen Content(in mg/kg).\n"\
                        f"2. Phosphorus Content(in mg/kg).\n"\
                        f"3. Potassium Content(in mg/kg).\n"\
                        f"4. pH of the Soil (in 1 to 14).\n"\
                        f"5. Annual Rainfall (in mm).\n"\

            response.message(message_body1)
            response.message(message_body2)
            
        elif params:
            no_of_params=5
            p = convert(params)
            p_func = []
            for i in range(0,no_of_params):
                print(float(p[i]))
                p_func.append(float(p[i]))
            message_body = model_predict(p_func[0],p_func[1], p_func[2],request.session['temp'],request.session['humid'],p_func[3],p_func[4],request)
            response.message(message_body) 
        else:
            response.message("Send your Location")
    
    return HttpResponse(response.to_xml(), content_type='text/xml')


def convert(lst): 
    return ''.join(lst).split("\n")