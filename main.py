# Python script to find free slots to get a CoVID-19 vaccination in India
# Based on the APIs available at https://apisetu.gov.in/public/marketplace/api/cowin
# Author: Raghu Ganapathy
# E-mail: raghu.1999@gmail.com

# UX Edit: Vishal Verma
# E-mail: vecbhopal@gmail.com

import requests
import pygame
import json
import datetime
import time
from requests.models import to_native_string

from requests.sessions import session

from os import system, name

BLR = '294'
BangaloreRural = '276'
BangaloreUrban = '265'

pygame.init()
pygame.mixer.init()
sounda = pygame.mixer.Sound("beep-01a.wav")

headers = {
    ':authority': 'cdn-api.co-vin.in',
    ':method': 'GET',
    ':scheme': 'https',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'dnt': '1',
    'if-none-match': 'W/"2a609-8B8UNv2+uURxPaIuHDntG9G6k6c"',
    'origin': 'https://www.cowin.gov.in',
    'referer': 'https://www.cowin.gov.in/',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
}

def clear():
  
    # for windows
    if name == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def audio_alert():
    sounda.play()


def hdl_time(week_no):
    today = datetime.date.today()
    next_date = today + datetime.timedelta(weeks=week_no)
    next_date = next_date.strftime('%d-%m-%Y')
    chk_date = str(next_date)
    return chk_date


def hdl_request(place, week_no):
    preamble = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id='
    link = preamble + place + '&date=' + hdl_time(week_no)
    response = requests.get(link, headers={
        # ':authority': 'cdn-api.co-vin.in',
        # ':method': 'GET',
        # ':scheme': 'https',
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'dnt': '1',
        'if-none-match': 'W/"2a609-8B8UNv2+uURxPaIuHDntG9G6k6c"',
        'origin': 'https://www.cowin.gov.in',
        'referer': 'https://www.cowin.gov.in/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    })
    #response = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=395&date=02-05-2021')
    print(hdl_time(week_no),"\t\t",end=""),
    data = response.json()

    no_of_centers = len(data["centers"])
    print(str(no_of_centers),"\t\t",end=""),
    #print('\t'),
    ref_id = []
    ref_id_age = []

    for i in range(0, no_of_centers):

        sample = data["centers"][i]
        sessions_data = sample["sessions"]
        sessions_data = sessions_data[0]
        available = sessions_data["available_capacity"]
        if available > 0:
            ref_id.append(i)

    no_vacc_centers = len(ref_id)
    print(str(no_vacc_centers),"\t\t",end=""),
    for i in ref_id:
        age = data["centers"][i]["sessions"][0]["min_age_limit"]
        if age == 18:
            ref_id_age.append(i)
    no_vacc_centers_18yo = len(ref_id_age)
    print(str(no_vacc_centers_18yo))
    if no_vacc_centers_18yo > 0:
        for i in ref_id_age:
                audio_alert()
                print(data["centers"][i])


if __name__ == "__main__":
    no_of_weeks = 10
    while True:
        clear()
        print('***********************************************')
        print('Checking for free slots in BLR-BBMP at', datetime.datetime.now())
        print('-------------------------------------------')
        print("Week starting\tTotal Centers\tAll Centers\t18+ Centers")
        for week in range(0, no_of_weeks):
            hdl_request(BLR, week)

        print()
        print('***********************************************')
        print('Checking for free slots in BLR-URBAN at', datetime.datetime.now())
        print('-------------------------------------------')
        print("Week starting\tTotal Centers\tAll Centers\t18+ Centers")
        for week in range(0, no_of_weeks):
            hdl_request(BangaloreUrban, week)

        print()
        print('***********************************************')
        print('Checking for free slots in BLR-RURAL at', datetime.datetime.now())
        print('-------------------------------------------')
        print("Week starting\tTotal Centers\tAll Centers\t18+ Centers")
        for week in range(0, no_of_weeks):
            hdl_request(BangaloreRural, week)

        time.sleep(30)

