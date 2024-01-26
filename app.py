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
        
        #Source input
        source_options = ['Bangalore', 'Kolkata', 'Delhi', 'Chennai', 'Mumbai']
        Source = st.selectbox("Source", source_options)

        
        
        # Departure time input
        default_time = datetime.now().replace(hour=0, minute=0)
        Dep_Time = st.time_input("Select Departure Time", value=default_time)
            
        # Extract hour from Dep_Time
        Dep_Hour = Dep_Time.hour
        # Extract minute from Dep_Time
        Dep_Minutes = Dep_Time.minute
        
        #Total Stops input
        Total_Stops = st.selectbox('Total_Stops',('non-stop', '1 stop','2 stops', '3 stops', '4 stops'))
        
    with col2:
        # Date of Journey input
        today = datetime.now()
        Date_of_Journey = st.date_input("Select Date of Journey", today)
        
        # Extract day and month
        Journey_day = Date_of_Journey.day
        Journey_month = Date_of_Journey.month
        
        # Check if the selected date is not before today
        if Date_of_Journey < today.date():
            st.warning("Please select a date not before today.")
            st.stop()  # Stop execution if the date is before today
        
        #Destination input
        source_options = ['Bangalore', 'Kolkata', 'Delhi', 'Chennai', 'Mumbai']
        destination_options = [city for city in source_options if city != Source]
        Destination = st.selectbox("Destination", destination_options)
        
        # Arrival time input
        default_time = datetime.now().replace(hour=0, minute=0)
        Arrival_Time = st.time_input("Select Arrival Time", value=default_time)
        
        # Check if the selected arrival time is later than departure time
        # Check if the selected arrival time is earlier than or equal to departure time
    
    # Extract hour from Arrival_Time
    Arrival_Hour = Arrival_Time.hour
    # Extract minute from Dep_Time
    Arrival_Minutes = Arrival_Time.minute

    # Check if arrival time is on the next day and adjust if necessary
    if Arrival_Time > Dep_Time:
        Duration_Hours = Arrival_Hour - Dep_Hour
        Duration_Minutes = Arrival_Minutes - Dep_Minutes
    else:
        # Arrival time is on the next day, add 24 hours to the duration
        Duration_Hours = 23 + Arrival_Hour - Dep_Hour
        Duration_Minutes = 60 + Arrival_Minutes - Dep_Minutes
        
    # Additional conditions to check and adjust Duration_Hours and Duration_Minutes
    if(Source == 'Bangalore' or Source == 'Delhi') and (Destination == 'Delhi' or Destination == 'Bangalore'):
        if Duration_Hours < 2 or (Duration_Hours == 2 and Duration_Minutes < 30):
            st.warning("The minimum duration needs to be 2 hr 30 minutes.")
            st.stop()  # Stop execution and show the warning message
    elif (Source == 'Bangalore' or Source == 'Kolkata') and (Destination == 'Kolkata' or Destination == 'Bangalore'):
        if Duration_Hours < 2 or (Duration_Hours == 2 and Duration_Minutes < 20):
            st.warning("The minimum duration needs to be 2 hr 20 minutes.")
            st.stop()  # Stop execution and show the warning message
    elif (Source == 'Bangalore' or Source == 'Chennai') and (Destination == 'Chennai' or Destination == 'Bangalore'):
        if (Duration_Hours< 1 and Duration_Minutes < 59):
            st.warning("The minimum duration needs to be 59 minutes.")
            st.stop()  # Stop execution and show the warning message
    elif (Source == 'Bangalore' or Source == 'Mumbai') and (Destination == 'Mumbai' or Destination == 'Bangalore'):
        if Duration_Hours < 1 or (Duration_Hours == 1 and Duration_Minutes < 50):
            st.warning("The minimum duration needs to be 1 hr 50 minutes.")
            st.stop()  # Stop execution and show the warning message
    elif (Source == 'Kolkata' or Source == 'Delhi') and (Destination == 'Delhi' or Destination == 'Kolkata'):
        if Duration_Hours < 2 or (Duration_Hours == 2 and Duration_Minutes < 25):
            st.warning("The minimum duration needs to be 2 hr 25 minutes.")
            st.stop()  # Stop execution and show the warning message
    elif (Source == 'Kolkata' or Source == 'Chennai') and (Destination == 'Chennai' or Destination == 'Kolkata'):
        if Duration_Hours < 2 or (Duration_Hours == 2 and Duration_Minutes < 25):
            st.warning("The minimum duration needs to be 2 hr 25 minutes.")
            st.stop()  # Stop execution and show the warning message
    elif (Source == 'Kolkata' or Source == 'Mumbai') and (Destination == 'Mumbai' or Destination == 'Kolkata'):
        if Duration_Hours < 2 or (Duration_Hours == 2 and Duration_Minutes < 35):
            st.warning("The minimum duration needs to be 2 hr 35 minutes.")
            st.stop()  # Stop execution and show the warning message
    elif (Source == 'Chennai' or Source == 'Mumbai') and (Destination == 'Mumbai' or Destination == 'Chennai'):
        if Duration_Hours < 1 or (Duration_Hours == 1 and Duration_Minutes < 55):
            st.warning("The minimum duration needs to be 1 hr 55 minutes.")
            st.stop()  # Stop execution and show the warning message
    elif (Source == 'Chennai' or Source == 'Delhi') and (Destination == 'Delhi' or Destination == 'Chennai'):
        if Duration_Hours < 2 or (Duration_Hours == 2 and Duration_Minutes < 50):
            st.warning("The minimum duration needs to be 2 hr 50 minutes.")
            st.stop()  # Stop execution and show the warning message
    elif (Source == 'Delhi' or Source == 'Mumbai') and (Destination == 'Mumbai' or Destination == 'Delhi'):
        if Duration_Hours < 2 or (Duration_Hours == 2 and Duration_Minutes < 10):
            st.warning("The minimum duration needs to be 2 hr 10 minutes.")
            st.stop()  # Stop execution and show the warning message
        
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

if st.button('Predict'):
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
    
    st.subheader('The arrival time is of the next date.')
    
    file = open('flight_model.pkl', 'rb')
    model = pickle.load(file)
    file.close()
    user_prediction = model.predict(fare_data)
    # Round off the predicted fare to two decimals
    rounded_prediction = round(user_prediction[0], 2)

    # Display the prediction in Streamlit
    
    st.markdown(f'<p style="font-size:40px;">Predicted Fare: <strong>INR {rounded_prediction}</strong></p>', unsafe_allow_html=True)
    
    
