import json

def adjust_population_area(json_file_path, output_file_path=None):

    with open(json_file_path, 'r', encoding='utf-8') as file:
        countries = json.load(file)

    for country in countries:
        population = country.get('population')
        area = country.get('area')
        if area and area != 0:
            country['population_density'] =  round(population / area, 1)
        else:
            country['population_density'] = None
        
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(countries, file, ensure_ascii=False, indent=4)

    print(f"✓ Population density added to each country.")

if __name__ == "__main__":
    input_file = "countriesListOutput.json"
    output_file = "adjustedCountriesListOutput.json"
    adjust_population_area(input_file, output_file)