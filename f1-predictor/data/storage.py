from datetime import datetime
import os
import pandas as pd

# Define classes for each CSV
class Driver:
    # driver,dob,first_race_date,driver_nationality
    def __init__(self, driver,dob,first_race_date,driver_nationality):
        self.driver = driver
        self.dob = datetime.strptime(dob, '%Y-%m-%d')
        self.first_race_date = datetime.strptime(first_race_date, '%Y-%m-%d')
        self.driver_nationality = driver_nationality

class Circuit:
    #circuit,type_circuit,circuit_nationality
    def __init__(self, circuit,type_circuit,circuit_nationality):
        self.circuit = circuit
        self.type_circuit = type_circuit
        self.circuit_nationality = circuit_nationality

class Constructor:
    #constructor,constructor_nationality
    def __init__(self, constructor,constructor_nationality):
        self.constructor = constructor
        self.constructor_nationality = constructor_nationality

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct absolute paths to the CSV files
driver_csv_path = os.path.join(current_dir, 'unique_driver_data.csv')
circuit_csv_path = os.path.join(current_dir, 'unique_circuit_data.csv')
constructor_csv_path = os.path.join(current_dir, 'unique_constructor_data.csv')

# Load data from CSV files
df1 = pd.read_csv(driver_csv_path)
df2 = pd.read_csv(circuit_csv_path)
df3 = pd.read_csv(constructor_csv_path)


# Convert rows to objects and store in lists
drivers = [Driver(**row) for row in df1.to_dict(orient='records')]
circuits = [Circuit(**row) for row in df2.to_dict(orient='records')]
constructors = [Constructor(**row) for row in df3.to_dict(orient='records')]


# Example: Accessing data from the lists
# print(list1[0].attribute_name)