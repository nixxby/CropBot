import calendar
from datetime import datetime

import requests
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


import requests, json   
api_key = "d0a2301b1066be60a90b946462380bab"

import warnings
warnings.filterwarnings('ignore')
#

def get_weather(lat, lon, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?lat="
    complete_url = base_url + lat + "&lon=" + lon + "&appid=" + api_key 
    # api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
    weather_response = requests.get(complete_url).json()
    print(weather_response)
    return weather_response


def generate_weather_params(weather_response):
    current_weather = {
        "temperature": round(int(weather_response["main"]["temp"])-273.15,2),
        "humidity": round(int(weather_response["main"]["humidity"]),2),
        "location": weather_response["name"],
        "description": weather_response["weather"][0]["description"],
    }

    return current_weather

#
def model_predict(N,P,K,temp,humid,ph,rain,request):
    with open(r"C:\Users\Nikhil Bhamwani\Desktop\Crop recommendation system\CropBot\venv\bot\Crop_recommendation.csv", 'r', newline='') as csvfile:
        df = pd.read_csv(csvfile)
        
        params = df[['N', 'P','K','temperature', 'humidity', 'ph', 'rainfall']]
        labels = df['label']
        crops = df['label'].unique()
        crops = sorted(crops)
        Xtrain, Xtest, Ytrain, Ytest = train_test_split(params,labels,test_size = 0.2,random_state =2)
        
        LogReg = LogisticRegression(random_state=2)
        LogReg.fit(Xtrain,Ytrain)

        predicted_values = LogReg.predict(Xtest)

        x = metrics.accuracy_score(Ytest, predicted_values)
        print("Logistic Regression's Accuracy is: ", round(x*100.000,3),"%.")

        data = np.array([[N,P,K, temp, humid, ph,rain]])

        prediction = LogReg.predict_proba(data)
        probabilities = prediction[0]
        probabilities =sorted(probabilities, reverse=True)
        print("These are the top 3 crops you should plant: ")
        probs= [0,0,0]
        for i in range (0,3):
            probs[i] = round(probabilities[i],3)*100
            print(i+1,") ",crops[prediction[0].tolist().index(probabilities[i])],"having a predicted probability of:",round(probabilities[i],2)*100,"%." )
        
        if probs[1]<2:
            message_body = f" *Crop Prediction on your soil* \n \n"\
                           f"{crops[prediction[0].tolist().index(probabilities[0])]}: {probs[0]}%.\n"\
        
        elif probs[2]<5:
            message_body = f" *Crop Prediction on your soil* \n \n"\
                f"{crops[prediction[0].tolist().index(probabilities[0])]}: {probs[0]}%.\n"\
                f"{crops[prediction[0].tolist().index(probabilities[1])]}: {probs[1]}%.\n"\
        
        else:
            message_body = f" *Crop Prediction on your soil* \n \n"\
                           f"{crops[prediction[0].tolist().index(probabilities[0])]}: {probs[0]}%.\n"\
                           f"{crops[prediction[0].tolist().index(probabilities[1])]}: {probs[1]}%.\n"\
                           f"{crops[prediction[0].tolist().index(probabilities[2])]}: {probs[2]}%.\n"\
                            
        return message_body