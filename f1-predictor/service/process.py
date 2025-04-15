import pandas as pd
import pickle
import os
from flask import Flask, request, jsonify
from data.storage import  drivers, circuits, constructors

current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the model file
rf_model_path = os.path.join(current_dir, 'rf.pkl')

rf_model = pickle.load(open(rf_model_path, "rb"))

def process_input_json(input_json):
    # Extract fields from the input JSON
    date = input_json.get("date")
    quali_pos = input_json.get("quali_pos")
    constructor = input_json.get("constructor")
    circuit = input_json.get("circuit")
    driver = input_json.get("driver")
    rain = input_json.get("rain")
    laps = input_json.get("laps")

    driver_obj = None
    circuit_obj = None
    constructor_obj = None

    if driver in [d.driver for d in drivers]:
        driver_obj = next(d for d in drivers if d.driver == driver)
    else:
        raise ValueError(f"Driver {driver} not found in the data.")

    if circuit in [c.circuit for c in circuits]:
        circuit_obj = next(c for c in circuits if c.circuit == circuit)
    else:
        raise ValueError(f"Circuit {circuit} not found in the data.")

    if constructor in [con.constructor for con in constructors]:
        constructor_obj = next(con for con in constructors if con.constructor == constructor)
    else:
        raise ValueError(f"Constructor {constructor} not found in the data.")

    age_at_gp_in_days = (pd.to_datetime(date) - driver_obj.dob).days
    days_since_first_race = (pd.to_datetime(date) - driver_obj.first_race_date).days

    # Create a dictionary to hold the processed data
    processed_data = {
        "year": pd.to_datetime(date).year,
        "quali_pos": quali_pos,
        "constructor": constructor,
        "circuit": circuit,
        "type_circuit": circuit_obj.type_circuit,
        "driver": driver,
        "age_at_gp_in_days": age_at_gp_in_days,
        "days_since_first_race": days_since_first_race,
        "rain": rain,
        "circuit_nationality": circuit_obj.circuit_nationality,
        "driver_nationality": driver_obj.driver_nationality,
        "constructor_nationality": constructor_obj.constructor_nationality,
        "driver_home": int(driver_obj.driver_nationality == circuit_obj.circuit_nationality),
        "constructor_home": int(constructor_obj.constructor_nationality == circuit_obj.circuit_nationality),
        "laps": laps
    }

    return processed_data

def process_input_json_multiple(input_json_list):
    processed_data_list = []

    for input_json in input_json_list:
        print(input_json)
        # Extract fields from the input JSON
        date = input_json.get("date")
        quali_pos = input_json.get("quali_pos")
        constructor = input_json.get("constructor")
        circuit = input_json.get("circuit")
        driver = input_json.get("driver")
        rain = input_json.get("rain")
        laps = input_json.get("laps")

        driver_obj = None
        circuit_obj = None
        constructor_obj = None

        if driver in [d.driver for d in drivers]:
            driver_obj = next(d for d in drivers if d.driver == driver)
        else:
            raise ValueError(f"Driver {driver} not found in the data.")

        if circuit in [c.circuit for c in circuits]:
            circuit_obj = next(c for c in circuits if c.circuit == circuit)
        else:
            raise ValueError(f"Circuit {circuit} not found in the data.")

        if constructor in [con.constructor for con in constructors]:
            constructor_obj = next(con for con in constructors if con.constructor == constructor)
        else:
            raise ValueError(f"Constructor {constructor} not found in the data.")

        if not driver_obj.dob or not driver_obj.first_race_date:
            raise ValueError(f"Driver {driver} has missing date information.")

        age_at_gp_in_days = (pd.to_datetime(date) - driver_obj.dob).days
        days_since_first_race = (pd.to_datetime(date) - driver_obj.first_race_date).days

        # Create a dictionary to hold the processed data
        processed_data = {
            "year": pd.to_datetime(date).year,
            "quali_pos": quali_pos,
            "constructor": constructor,
            "circuit": circuit,
            "type_circuit": circuit_obj.type_circuit,
            "driver": driver,
            "age_at_gp_in_days": age_at_gp_in_days,
            "days_since_first_race": days_since_first_race,
            "rain": rain,
            "circuit_nationality": circuit_obj.circuit_nationality,
            "driver_nationality": driver_obj.driver_nationality,
            "constructor_nationality": constructor_obj.constructor_nationality,
            "driver_home": int(driver_obj.driver_nationality == circuit_obj.circuit_nationality),
            "constructor_home": int(constructor_obj.constructor_nationality == circuit_obj.circuit_nationality),
            "laps": laps
        }

        processed_data_list.append(processed_data)

    return processed_data_list
def rf_predict(df):
    prediction = rf_model.predict(df)
    return prediction
