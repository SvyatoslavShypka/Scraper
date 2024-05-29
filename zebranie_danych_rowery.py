import pandas as pd
import glob
import os

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Ścieżka do folderu z plikami CSV
    folder_path = 'Data'

    # Wyszukiwanie wszystkich plików CSV w folderze
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

    # Lista do przechowywania DataFrame'ów
    dfs = []

    # Iteracja po wszystkich plikach CSV i ich wczytywanie
    for file in csv_files:
        df = pd.read_csv(file)
        dfs.append(df)

    # Łączenie wszystkich DataFrame'ów w jeden
    combined_df = pd.concat(dfs, ignore_index=True)

    # Konwersja kolumny 'Data wynajmu' na format datetime
    combined_df['Data wynajmu'] = pd.to_datetime(combined_df['Data wynajmu'])

    # Wyciąganie tylko daty (bez czasu) z kolumny 'Data wynajmu'
    combined_df['Data wynajmu'] = combined_df['Data wynajmu'].dt.date

    # Konwersja kolumny 'Czas trwania' na typ liczbowy (jeśli nie jest już liczbą)
    combined_df['Czas trwania'] = pd.to_numeric(combined_df['Czas trwania'], errors='coerce')

    # Grupowanie po kolumnie 'Data wynajmu', liczenie liczby wynajmów na dzień i sumowanie 'Czas trwania'
    daily_rentals = combined_df.groupby('Data wynajmu').agg(
        {'UID wynajmu': 'size', 'Czas trwania': 'sum'}).reset_index()

    # Zmiana nazwy kolumny 'UID wynajmu' na 'Ilość wynajmów'
    daily_rentals.rename(columns={'UID wynajmu': 'Ilość wynajmów'}, inplace=True)

    # Zapisanie wyników do nowego pliku CSV
    output_file = 'daily_rentals_with_duration.csv'
    daily_rentals.to_csv(output_file, index=False)

    print(f'Dane zostały zapisane do pliku {output_file}')


