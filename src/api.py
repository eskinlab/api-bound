import csv
from datetime import datetime, timedelta
from flask import Flask, request

app = Flask(__name__)

INPUT_FILE = OUTPUT_FILE = "../input.csv"


# Function to calculate the success column for each flight
def calculate_success(arrival_time, departure_time, arrivals_today):
    if len(arrivals_today) >= 20:
        return 'fail'
    else:
        if (departure_time - arrival_time) >= timedelta(minutes=180):
            return 'success'
        else:
            return 'fail'


# Function to update the success column in the flights CSV file
def update_success_column(file):
    flights = []
    with open(file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row = {k.strip(): v.strip() for k, v in row.items()}
            flights.append(row)

    arrivals_today = []
    for flight in flights:
        arrival_time = datetime.strptime(flight['Arrival'], '%H:%M')
        departure_time = datetime.strptime(flight['Departure'], '%H:%M')
        success = calculate_success(arrival_time, departure_time, arrivals_today)
        flight['success'] = str(success)
        arrivals_today.append(flight)

    print(flights)
    with open(OUTPUT_FILE, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=['flight ID', 'Arrival', 'Departure', 'success'])
        writer.writeheader()
        writer.writerows(flights)


# GET API endpoint to get info about a flight
@app.route('/flight/<flight_id>', methods=['GET'])
def get_flight_info(flight_id):
    with open(OUTPUT_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['flight ID'] == flight_id:
                return f"Flight info: {row}"
        else:
            return {'message': 'Flight not found'}, 404


# POST API endpoint to update the csv file with flights as an input
@app.route('/flight', methods=['POST'])
def update_flights():
    flight_id = request.form.get('flight ID')
    arrival_time = request.form.get('Arrival')
    departure_time = request.form.get('Departure')
    with open(OUTPUT_FILE, 'a') as file:
        writer = csv.writer(file)
        writer.writerow([flight_id, arrival_time, departure_time, ''])

    update_success_column(OUTPUT_FILE)

    return {'message': 'Flight added successfully'}


if __name__ == '__main__':
    update_success_column(INPUT_FILE)
    app.run()
