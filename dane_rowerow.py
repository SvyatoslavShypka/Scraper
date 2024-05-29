import requests
import pandas as pd

# Funkcja do pobierania danych z CKAN API za pomocą zapytania SQL
def fetch_data_sql(sql):
    url = 'https://www.wroclaw.pl/open-data/api/action/datastore_search_sql'
    params = {'sql': sql}
    response = requests.get(url, params=params)
    response.raise_for_status()  # Sprawdza, czy nie było błędów
    return response.json()

if __name__ == '__main__':
    # Zapytanie SQL do pobrania danych za dzień 2023-11-05
    sql_query = "SELECT * FROM \"c737af89-bcf7-4f7d-8bbc-4a0946d7006e\" WHERE \"Data wynajmu\" >= '2023-11-05' AND \"Data wynajmu\" < '2023-11-06'"

    # Pobieranie danych za pomocą zapytania SQL
    data = fetch_data_sql(sql_query)
    records = data['result']['records']

    # Konwersja danych do DataFrame
    df = pd.DataFrame.from_records(records)

    # Zamiana kolumn
    df = df[['Data wynajmu'] + [col for col in df.columns if col != 'Data wynajmu']]

    # Zapis DataFrame do pliku CSV
    df.to_csv('dane_rowerowe_2023-11-05.csv', index=False)

    print('Pobrano i zapisano dane za dzień 2023-11-05 do pliku dane_rowerowe_2023-11-05.csv')
