import requests
import json

api_url = "https://restcountries.com/v3.1/all?fields=name,population,area,gini,region"

def fetch_countries():
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return [f"Error: {response.status_code} - {response.text}"]
    
if __name__ == "__main__":
    countries = fetch_countries()

    output_file = "countriesListOutput.json"
    with open(output_file, "w") as json_file:
        json.dump(countries, json_file, indent=4)
    print (f"Data written to {output_file}")