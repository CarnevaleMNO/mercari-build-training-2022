import requests
import json

def translate_api(item_name):
  url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

  payload = "q=" + item_name + "&target=ja&source=en"
  headers = {
    "content-type": "application/x-www-form-urlencoded",
    "Accept-Encoding": "application/gzip",
    "X-RapidAPI-Host": "google-translate1.p.rapidapi.com",
    "X-RapidAPI-Key": "ecad780f8emsh4be70dd8431b5d5p181387jsndea9fa424723"
  }

  response = requests.request("POST", url, data=payload, headers=headers)
  json_data = json.loads(response.text)
  return json_data["data"]["translations"][0]["translatedText"]