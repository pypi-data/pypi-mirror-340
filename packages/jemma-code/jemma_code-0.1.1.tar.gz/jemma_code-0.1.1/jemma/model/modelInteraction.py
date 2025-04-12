import json
import requests

from jemma.utils.getApiKey import get_api_key
from jemma.utils.terminalPrettifier import errorText, warningText
from requests.exceptions import RequestException
from jemma.config import CONFIG 
def modelInteraction(prompt: str, isJsonResponse: bool = False):
 try:
    payload = {
            "system_instruction": {
                "parts": [
                    {
                        "text": "You are Jemma, a command line coding assistant. Make sure your responses are always helpful, friendly, and concise"
                    }
                ]
            },
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                            
                        }
                    ]
                }
            ]
        }
        
    apikey = get_api_key()
    generationConfig = {}
    if isJsonResponse:
        generationConfig["response_mime_type"]= "application/json"
    generationConfig["temperature"]=CONFIG.temperature
    if CONFIG.max_output_tokens != 0 : ##so basically, user has not set a max token output
       generationConfig["maxOutputTokens"] = CONFIG.max_output_tokens
    payload["generationConfig"] = generationConfig
    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{CONFIG.model}:generateContent?key={apikey}",
        headers={'Content-Type': "application/json"},
        data=json.dumps(payload)
    )
    response_data = response.json()
 
    if response.status_code == 400:
       print(errorText("Error occured, Your api key likely isn't valid, run")+warningText(' jemma-configure ')+ errorText('to re-enter your key'))
       return None
    if response.status_code != 200:
        print(errorText('An error occured, please try again in a bit'))
        print (str(response.status_code))
        return None
    if 'candidates' in response_data and len(response_data['candidates']) > 0:
        response=  response_data['candidates'][0]['content']['parts'][0]['text']
        return response
    else:
        print(errorText('something went wrong and the model did not return a response'))    
        return None  
 except RequestException:
    print(errorText("You need a working Internet Connection to use jemma"))
    return None
 except Exception as e:
    print(errorText('An unexpected error occured, please try again' + str(e)))
    return None