import time

import requests
from datetime import datetime
import smtplib

MY_LAT = 1
MY_LONG = 1

MY_PASSWORD = ""
MY_EMAIL = ""

parameters_sunset = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}


def is_above():
    my_lat_plus = MY_LAT + 5
    my_lat_min = MY_LAT - 5
    my_long_plus = MY_LONG + 5
    my_long_min = MY_LONG - 5
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if ((my_lat_min <= iss_latitude <= my_lat_plus) and (my_long_min <= iss_longitude <= my_long_plus)
            and ()):
        return True
    else:
        return False


def is_night():
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters_sunset)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    hour_now = int(datetime.now().hour)
    if sunset <= hour_now <= sunrise:
        return True
    else:
        return False


while True:
    time.sleep(60)
    if is_night() and is_above():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL,MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addr=MY_EMAIL,
            msg="Subject:Look Up\n\n The ISS above you in the sky.")

