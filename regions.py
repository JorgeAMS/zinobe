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


def get_country(regions, time1):
    
    my_regions = {}
    regions_dt = {'region':[], 'country':[], 'language':[], 'time':[]}

    for reg in regions:
        url = f"https://restcountries.eu/rest/v2/region/{reg}"
        response = requests.request("GET", url)

        time2= time1 + response.elapsed.total_seconds()

        r = response.json()[0]
        country=r['name']
        language=r['languages'][0]['name']
        lang_SHA1= hashlib.sha1(language.encode('utf-8')).hexdigest()

        my_regions[reg]={country:{"language":language}}

        regions_dt['region'].append(reg)
        regions_dt['country'].append(country)
        regions_dt['language'].append(lang_SHA1)
        regions_dt['time'].append(time2)
    
    return my_regions, regions_dt


if __name__ == "__main__":
    regions = []
    my_regions = {}
    regions_dt = {}

    regions, time1 = get_regions()
    my_regions, regions_dt = get_country(regions, time1)



