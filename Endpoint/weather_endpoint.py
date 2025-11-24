import os
import xml.etree.ElementTree as ET
from support import download_get_url


def remove_diacriticism(name):
        chars_replace = [ ["á","a"], ["é","e"], ["í","i"], ["ó","o"], ["ú","u"], ["ů","u"], ["ý","y"], ["č","c"], ["ď","d"], ["ě","e"], ["ň","n"], ["š","s"], ["ť","t"], ["ž","z"], ["ř","r"] ]
        for char_replace in chars_replace:
            name = name.replace(char_replace[0], char_replace[1])
        return name

def get_gps_from_xml(xml):
    """
    Vytažení GPS souřadnic z XML
    """
    tree = ET.ElementTree(ET.fromstring(xml))
    root = tree.getroot()
    lat = 0
    lng = 0
    status = ""
    for child in root:
        if child.tag == "status":
            status = child.text
        if child.tag == "result":
            for child2 in child:
                if child2.tag == "geometry":
                    for child3 in child2:
                        if child3.tag == "location":
                            for child4 in child3:
                                if child4.tag == "lat":
                                    lat = child4.text
                                if child4.tag == "lng":
                                    lng = child4.text
    if status == "OK":
        lat = float(lat)
        lng = float(lng)
    return (lat, lng)

def get_weather_place_by_name_endpoint(client, place_name):
    """
    Najde souřadnice pro danou lokalitu
    """
    place_location = client.from_("weather_place").select("*").filter("place_name", "ilike", place_name).execute()
    lat = 0
    lng = 0
    if len(place_location.data) == 0 or not place_location.data[0]["place_lat"] or not place_location.data[0]["place_lon"]:
        place_name_goolge = place_name.lower()
        place_name_goolge = remove_diacriticism(place_name_goolge)
        app_google_api = os.getenv("APP_GOOGLE_API")
        google_api_geocode_url = os.getenv("GOOGLE_API_GEOCODE_URL")
        url = google_api_geocode_url.format(place_name_goolge=place_name_goolge, app_google_api=app_google_api)
        body = download_get_url(url, ())
        lat, lng = get_gps_from_xml(body)
        if lat != 0 and lng != 0:
            insert_data = {
                "place_name": place_name,
                "place_lat": lat,
                "place_lon": lng
            }
            client.from_("weather_place").insert(insert_data).execute()
            place_location = client.from_("weather_place").select("*").filter("place_name", "ilike", place_name).execute()
    return place_location.data[0]

