import requests
import hashlib
import sqlite3
import json
import pandas


def get_regions():
    url = "https://restcountries-v1.p.rapidapi.com/all"                                 # URL to get the regions

    headers = {                                                             # Headers to make the request
        'x-rapidapi-key': "7c4f3a3762msh144ae6194839930p18a12ajsndd1c892fcda9",
        'x-rapidapi-host': "restcountries-v1.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers)                     # Gets all the regions                        

    time1= response.elapsed.total_seconds()                                 # Gets the time the request takes to get the regions

    regions = []                                              # list to store the regions

    for r in response.json():
        region = r['region']                                                            
        if region not in regions and region != "":                 # Conditional statement to avoid storing one region several times
            regions.append(region)
    
    return regions, time1


def get_country(regions, time1):                                   ## Function to get the first country and the language for ech region
    
    my_regions = {}                                                       # Dictionary to structure data in json
    regions_dt = {'region':[], 'country':[], 'language':[], 'time':[]}          # dictionary to structure data as DataFrame

    for reg in regions:
        url = f"https://restcountries.eu/rest/v2/region/{reg}"            # URL to get country information per Region
        response = requests.request("GET", url)

        time2= time1 + response.elapsed.total_seconds()                      # Math to get the total time spent on requests

        r = response.json()[0]                                         # Gets the first country of the data
        country=r['name']                                          # Gets the name of the country
        language=r['languages'][0]['name']                               # Gets the first language for the country
        lang_SHA1= hashlib.sha1(language.encode('utf-8')).hexdigest()           # Encoding language as SHA1

        my_regions[reg]={country:{"language":language}}                         # Storing Region > Conutry > Language on 'my_regions' dict 

        regions_dt['region'].append(reg)                               # Appending region name to 'regions_dt' dict
        regions_dt['country'].append(country)                            # Appending country name to 'regions_dt' dict
        regions_dt['language'].append(lang_SHA1)                           # Appending language to 'regions_dt' dict
        regions_dt['time'].append(time2)                                # Appending total time to 'regions_dt' dict
    
    return my_regions, regions_dt


def get_dataframe(regions_dt):                      ## Function to convert a dictionary to a Pandas DataFrame, inserting the dataframe into a sqlite3 db, pintring results & time
        
    cnx = sqlite3.connect('regions.db')                         # Connection to the local db file

    data=pandas.DataFrame.from_dict(regions_dt)                 # Converting the dictionary 'regions_dt' to Pandas DataFrame
    data.to_sql(name='data', con=cnx, if_exists='replace')          # Saving data into regions.db

    cnx.close()                                     # Closing db connection
    print(data)                                     # printing DataFrame Table

    print("\n\n"+"{:<10} {:<10} {:<10} {:<10}".format("Max time", "Min time", "Average", "Total"))                  # Pinting Max, Min, average and total time
    print("{:<10} {:<10} {:<10} {:<10}".format(round(data["time"].max(),4), round(data["time"].min(),4), round(data["time"].mean(),4), round(data["time"].sum(),4)))


def get_json(my_regions):               ## Function to create a json file from a dictionary
    f = open("data.json", "w", encoding="utf-8")              
    f.write(json.dumps(my_regions, indent=4, ensure_ascii=False))       # Saving the dictionary 'my_regions' into data.json file, in Json format
    f.close()


if __name__ == "__main__":

    regions, time1 = get_regions()
    my_regions, regions_dt = get_country(regions, time1)
    get_dataframe(regions_dt)
    get_json(my_regions)
