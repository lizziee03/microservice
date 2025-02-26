# server side

import zmq, requests, json, datetime, time

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5000")

while True:
    API_key = ""
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    city_name = socket.recv_string()
    print("Obtaining date, time and weather data for " + city_name + "...")
    complete_url = base_url + "appid=" + API_key + "&q=" + city_name + "&units=imperial"
    response = requests.get(complete_url)

    res = response.json()

    if res["cod"] != "404":
        main = res["main"]
        
        temperature = main["temp"]
        temp_feels_like = main["feels_like"]

        weather = res["weather"]
        
        timezone = res["timezone"]

        weather_description = weather[0]["description"]
    else:
        print("city data not found")

    weekday_mapping = ("Monday", "Tuesday", "Wednesday", "Thursday",
                        "Friday", "Saturday", "Sunday")

    tz = datetime.timezone(datetime.timedelta(seconds=int(timezone)))
    current_datetime_str = datetime.datetime.now(tz = tz).strftime("%m/%d/%Y, %H:%M:%S")
    weekday_int = datetime.datetime.now(tz = tz).weekday()
    current_weekday = weekday_mapping[weekday_int]

    response_data = ("In" + str(city_name) + " it is " + str(current_weekday) + 
    " and the date is " + str(current_datetime_str) + ". In " +
    str(city_name) + " the current temperature is " + str(temperature) +
    " but it feels like " + str(temp_feels_like) + " with " +
    str(weather_description) + ".")
    
    # response_data_arr = [city_name, current_datetime_str, current_weekday,
    # temperature, temp_feels_lilke, weather_description]
        
    socket.send_string(response_data)
