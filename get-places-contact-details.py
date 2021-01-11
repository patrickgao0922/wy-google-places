import requests
import json
import csv

# Global variables
apiKey = "AIzaSyAnYRkQ0oq-cBFTW9jLCznEPUyZO1gbzMU" # Google API Key
query = "Clothing+dresse+dress+fashion+ladies+lady+girl+girls+women+woman" # Query String
radius = 50000 # Radius from the coordination

# Coordinates
latitude = -37.840935
longitude = 144.946457

# How many pages to retrieve from Google API
pageNumber = 20
results = [] # Temporary place details list before writting into CSV file
nextPageToken = "" # Next page token

# Get the first page of place list with search query
def getFirstPage():
    placesResponse = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&location={},{}&radius={}&key={}".format(query, latitude, longitude, radius,apiKey))
    json = placesResponse.json()
    placesList = json["results"]
    global nextPageToken
    nextPageToken = json["next_page_token"]
    placeIDs = list(map(lambda x: x["place_id"], placesList))
    for placeID in placeIDs:
        getDetail(placeID)

# Get subsequent page of place list with next page token
def getNextPage():
    global nextPageToken
    placesResponse = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken={}&key={}".format(nextPageToken,apiKey))
    json = placesResponse.json()
    placesList = json["results"]
    if "next_page_token" in json:
        nextPageToken = json["next_page_token"]
    else:
        nextPageToken = None
    placeIDs = list(map(lambda x: x["place_id"], placesList))
    for placeID in placeIDs:
        getDetail(placeID)

# Get place details with place_id
def getDetail(placeID):
    detailResponse = requests.get("https://maps.googleapis.com/maps/api/place/details/json?place_id={}&fields=place_id,name,website,formatted_phone_number&key={}".format(placeID, apiKey))
    jsonResult = detailResponse.json()["result"]
    values = []
    values.append(jsonResult["place_id"]) if "place_id" in jsonResult else values.append("")
    values.append(jsonResult["name"]) if "name" in jsonResult else values.append("")
    values.append(jsonResult["formatted_phone_number"]) if "formatted_phone_number" in jsonResult else values.append("")
    values.append(jsonResult["website"]) if "website" in jsonResult else values.append("")
    encodedValues = list(map(lambda x: x.encode("utf-8"), values))
    results.append(encodedValues)

# Main logic
getFirstPage()
for i in range(pageNumber-1):
    if nextPageToken != None:
        getNextPage()

# Write final result into csv file
data_file = open('data_file.csv', 'w')
csv_writer = csv.writer(data_file)
csv_writer.writerows(results)
data_file.close()