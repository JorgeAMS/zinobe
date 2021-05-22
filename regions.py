import requests
import hashlib
import sqlite3
import json
import pandas


def get_regions():
    url = "https://restcountries-v1.p.rapidapi.com/all"

    headers = {
        'x-rapidapi-key': "7c4f3a3762msh144ae6194839930p18a12ajsndd1c892fcda9",
        'x-rapidapi-host': "restcountries-v1.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers)

    time1= response.elapsed.total_seconds()

    regions = []

    for r in response.json():
        region = r['region']
        if region not in regions and region != "":
            regions.append(region)
    
    return regions, time1


if __name__ == "__main__":
    regions = []
    my_regions = {}
    regions_dt = {'region':[], 'country':[], 'language':[], 'time':[]}

    regions, time1= get_regions()

