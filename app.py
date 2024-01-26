import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta  # Import the datetime class
import pickle

st.title('Flight Fare Prediction')

def user_input_features():
    col1, col2 = st.columns(2)
    with col1:
        Airline = st.selectbox('Airline',('IndiGo', 'Air India', 'Jet Airways', 'SpiceJet',
       'Multiple carriers', 'GoAir', 'Vistara', 'Air Asia',
       'Vistara Premium economy', 'Jet Airways Business',
       'Multiple carriers Premium economy', 'Trujet'))
        
        # Date of Journey input
        today = datetime.now()
        Date_of_Journey = st.date_input("Select Date of Journey", today)
        
        # Check if the selected date is not before today
        if Date_of_Journey < today.date():
            st.warning("Please select a date not before today.")
            st.stop()  # Stop execution if the date is before today

        # Extract day and month
        Journey_day = Date_of_Journey.day
        Journey_month = Date_of_Journey.month
        
        #Source input
        source_options = ['Bangalore', 'Kolkata', 'Delhi', 'Chennai', 'Mumbai']
        Source = st.selectbox("Source", source_options)
        
        #Destination input
        destination_options = [city for city in source_options if city != Source]
        Destination = st.selectbox("Destination", destination_options)
        
    with col2:
        # Departure time input
        Dep_Time = st.time_input("Select Departure Time")
            
        # Extract hour from Dep_Time
        Dep_Hour = Dep_Time.hour
        # Extract minute from Dep_Time
        Dep_Minutes = Dep_Time.minute
        
        # Arrival time input
        Arrival_Time = st.time_input("Select Arrival Time")
        
        # Check if the selected arrival time is later than departure time
        if Arrival_Time <= Dep_Time:
            st.warning("Arrival time should be later than Departure time.")
            st.stop()  # Stop execution if arrival time is not later than departure time
            
        # Extract hour from Arrival_Time
        Arrival_Hour = Arrival_Time.hour
        # Extract minute from Dep_Time
        Arrival_Minutes = Arrival_Time.minute
        
        Duration_Hours = Arrival_Hour - Dep_Hour
        Duration_Minutes = Arrival_Minutes - Dep_Minutes
        
        #Total Stops input
        Total_Stops = st.selectbox('Total_Stops',('non-stop', '1 stop','2 stops', '3 stops', '4 stops'))
        
    data = {'Total_Stops': Total_Stops,
            'Journey_day' : Journey_day,
            'Journey_month' : Journey_month,
            'Dep_Hour' : Dep_Hour,
            'Dep_Minute': Dep_Minutes,
            'Arrival_Hour': Arrival_Hour,
            'Arrival_Minute' : Arrival_Minutes,
            'Duration_Hours' : Duration_Hours,
            'Duration_Minutes' : Duration_Minutes,
            'Airline': Airline,
            'Source': Source,
            'Destination': Destination,
            }
    
    features = pd.DataFrame(data, index=[0])
    
    return features

input_df = user_input_features()

if st.button('Submit'):
    fare_data = pd.read_csv('train_data_processed.csv')
    fare_data = fare_data.drop(['Price'], axis=1)
    fare_data = pd.concat([input_df, fare_data], axis=0)

    Airline = pd.get_dummies(fare_data[['Airline']])
    Source = pd.get_dummies(fare_data[['Source']])
    Destination = pd.get_dummies(fare_data[['Destination']])
    fare_data.replace({'non-stop':0, '1 stop': 1, '2 stops': 2, '3 stops' : 3, '4 stops' : 4}, inplace=True)

    # Drop the Airline, Source, Destionation table
    fare_data.drop(['Airline', 'Source', 'Destination'], axis=1, inplace=True)
    #Add the OneHotEncoded Tables
    fare_data = pd.concat([fare_data, Airline, Source, Destination], axis=1)

    fare_data = fare_data[:1]  # Selects only the first row (the user input data)
    
    st.title('Predicton')
    
    file = open('flight_model.pkl', 'rb')
    model = pickle.load(file)
    file.close()
    user_prediction = model.predict(fare_data)

    # Display the prediction in Streamlit
    st.subheader('Flight Fare Prediction:')
    st.write('Predicted Fare: INR {}'.format(user_prediction[0]))
    
    
