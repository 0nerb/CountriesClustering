import json

def simplify_name_field(json_file_path, output_file_path=None):

    with open(json_file_path, 'r', encoding='utf-8') as f:
        countries = json.load(f)
    
    for country in countries:
        if isinstance(country['name'], dict) and 'official' in country['name']:
            country['name'] = country['name']['official']
    
    output = output_file_path or json_file_path

    with open(output, 'w', encoding='utf-8') as f:
        json.dump(countries, f, ensure_ascii=False, indent=4)
    
    print(f"✓ Transformação concluída! {len(countries)} países processados.")
    print(f"✓ Arquivo salvo em: {output}")
    
    return countries

def removing_gini_zeros(json_file_path, output_file_path=None):

    with open(json_file_path, 'r', encoding='utf-8') as f:
        countries = json.load(f)
    
    for country in countries[:]:
        gini = country.get('gini')
        if not gini or (isinstance(gini, (int, float)) and gini == 0):
            countries.remove(country)
    
    output = output_file_path or json_file_path
    
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(countries, f, ensure_ascii=False, indent=4)
    
    print("Removidos países com Gini igual a zero ou ausente.")
    
    return 0


if __name__ == "__main__":
    input_file = "countriesListOutput.json"

    simplify_name_field(input_file)
    removing_gini_zeros(input_file)
   