<H3> REST API for flights info </H3> 


Run the following command to install the packages:
```commandline
pip install -r requirements.txt
```

Run the following command to start the server:
```commandline
python.exe src/api.py
```
By default, the server starts on the localhost and port 5000.  

For testing purposes, you can use tools like Curl or Postman to send GET and POST requests to the API endpoints.  

To check GET request:
```commandline
curl -i -X GET http://127.0.0.1:5000/flight/B12
```
To check POST request:
```commandline
curl -i -X POST -d "flight ID=111&Arrival=01:20&Departure=6:20" http://127.0.0.1:5000/flight
curl -i -X GET http://127.0.0.1:5000/flight/111
```
