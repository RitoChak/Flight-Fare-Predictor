# Flight Fare Prediction Model

## To check the flight fare prediction website : [Click here](https://flight-fare-predictor.streamlit.app/)

This project involves the development of a machine learning model for predicting flight fares based on various input parameters. The model has been trained on historical flight data and utilizes a Random Forest Regressor algorithm for making predictions.

## Overview

- The project involves the following key steps:
  - Data Collection: The training data is obtained from an Excel file named `Data_Train.xlsx`.
  - Data Preprocessing: The collected data is cleaned and preprocessed to handle missing values and convert relevant columns into a suitable format.
  - Feature Engineering: Additional features are extracted from the existing data, such as the day and month of the journey, departure and arrival times, and duration of the flight.
  - Handling Categorical Data: One-hot encoding is applied to categorical features like airline, source, and destination.
  - Model Development: The Random Forest Regressor is chosen as the predictive model due to its ability to handle complex relationships in data.
  - Hyperparameter Tuning: The model undergoes hyperparameter tuning using techniques like Randomized Search CV to optimize its performance.
  - Model Evaluation: The model is evaluated using various metrics such as Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean Squared Error (RMSE), and R-squared.

## Usage

- The trained model is saved as a pickle file named `flight_model.pkl`.
- A Streamlit web application is created to facilitate user input for predicting flight fares.
- Users can input details such as airline, date of journey, source, destination, departure time, arrival time, and the number of stops.
- The application validates input data, ensuring that the date of journey is not before today, and the arrival time is later than the departure time.
- After submitting the input, the model predicts the flight fare, and the result is displayed to the user.

## Dependencies

- Python
- Libraries: NumPy, Pandas, Matplotlib, Seaborn, Scikit-learn, Streamlit

## Exploratory Data Analysis and Model Building
For a detailed analysis and model building process, you can refer to the [Jupyter Notebook.](Flight_Fare_Predictor.ipynb)

Feel free to contribute to the project or provide feedback!
