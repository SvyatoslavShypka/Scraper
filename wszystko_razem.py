import pandas as pd

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Wczytaj dane z plików CSV
    thw_data = pd.read_csv('thw_2023.csv')
    rain_data = pd.read_csv('rain.csv')
    rentals_data = pd.read_csv('daily_rentals_with_duration.csv')

    # Upewnij się, że kolumny z datami mają odpowiedni format
    thw_data['Date'] = pd.to_datetime(thw_data['Date']).dt.date
    rain_data['date'] = pd.to_datetime(rain_data['date']).dt.date
    rentals_data['Data wynajmu'] = pd.to_datetime(rentals_data['Data wynajmu']).dt.date

    # Zmień nazwy kolumn dla spójności przed scalaniem
    rain_data.rename(columns={'date': 'Date'}, inplace=True)
    rentals_data.rename(columns={'Data wynajmu': 'Date'}, inplace=True)

    # Wybierz tylko wymagane kolumny z plików thw_data i rain_data
    thw_data = thw_data[['Date', 'Avg Temperature', 'Avg Humidity', 'Avg Wind Speed']]
    rain_data = rain_data[['Date', 'prcp']]
    rentals_data = rentals_data[['Date', 'Ilość wynajmów', 'Czas trwania']]

    # Scal dane po kolumnie 'Date'
    merged_data = pd.merge(thw_data, rain_data, on='Date', how='left')
    merged_data = pd.merge(merged_data, rentals_data, on='Date', how='left')

    # Wypełnij brakujące wartości (opcjonalnie, w zależności od potrzeb)
    merged_data.fillna(0, inplace=True)

    # Wybierz tylko końcowe wymagane kolumny
    final_columns = ['Date', 'Avg Temperature', 'Avg Humidity', 'Avg Wind Speed', 'prcp', 'Ilość wynajmów',
                     'Czas trwania']
    final_data = merged_data[final_columns]

    # Zapisz wynikowy plik CSV
    final_data.to_csv('merged_data.csv', index=False)

    print('Dane zostały połączone i zapisane do pliku merged_data.csv')
