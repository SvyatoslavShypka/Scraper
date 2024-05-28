from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


def get_dates_from_url(url):
    parts = url.split('/')  # Rozbijamy URL na części
    year_month_str = parts[-1]  # Ostatnia część to rok i miesiąc
    year, month = map(int, year_month_str.split('-'))  # Dzielimy na rok i miesiąc
    num_days = pd.Timestamp(year, month, 1).days_in_month  # Obliczamy liczbę dni w miesiącu
    return [f'{year}{str(month).zfill(2)}{str(day).zfill(2)}' for day in range(1, num_days + 1)]  # Generujemy listę dat w odpowiednim formacie


if __name__ == '__main__':
    # URL strony z historią pogody dla Wrocławia w styczniu 2022 roku
    url = 'https://www.wunderground.com/history/monthly/pl/wroc%C5%82aw/EPWR/date/2022-1'
    dates = get_dates_from_url(url)

    # Ustawienie WebDrivera Selenium (załóżmy, że ChromeDriver znajduje się w ścieżce)
    service = Service("C:\\Install\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")  # Zaktualizuj tę ścieżkę do położenia ChromeDrivera
    driver = webdriver.Chrome(service=service)
    # Pobierz daty z linku URL

    try:
        # Otwórz stronę
        driver.get(url)

        # Poczekaj, aż tabela się załaduje
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.days.ng-star-inserted'))
        )


        # Wykonaj skrypt JavaScript do pobrania danych z tabeli
        table_data = driver.execute_script("""
            let rows = document.querySelectorAll('table.days.ng-star-inserted tbody tr');
            let data = [];
            rows.forEach(row => {
                let dateTable = row.querySelector('td:nth-child(1) table');
                let tempTable = row.querySelector('td:nth-child(2) table');
                let humidityTable = row.querySelector('td:nth-child(3) table'); // Załóżmy, że wilgotność jest w 3. kolumnie
                let windTable = row.querySelector('td:nth-child(4) table'); // Załóżmy, że prędkość wiatru jest w 4. kolumnie

                if (dateTable && tempTable && humidityTable && windTable) {
                    let dateCells = dateTable.querySelectorAll('tr');
                    let tempCells = tempTable.querySelectorAll('tr');
                    let humidityCells = humidityTable.querySelectorAll('tr');
                    let windCells = windTable.querySelectorAll('tr');

                    dateCells.forEach((dateCell, index) => {
                        let dateText = dateCell.querySelector('td').innerText.trim();
                        let avgTempText = tempCells[index].querySelectorAll('td')[1].innerText.trim(); // Dostosowane do kolumny 'Avg'
                        let avgHumidityText = humidityCells[index].querySelectorAll('td')[1].innerText.trim(); // Dostosowane do kolumny 'Avg'
                        let avgWindText = windCells[index].querySelectorAll('td')[1].innerText.trim(); // Dostosowane do kolumny 'Avg'
                        data.push([dateText, avgTempText, avgHumidityText, avgWindText]);
                    });
                }
            });
            return data;
        """)

        # Utwórz DataFrame na podstawie danych
        if table_data:
            df = pd.DataFrame(table_data, columns=['Date', 'Avg Temperature', 'Avg Humidity', 'Avg Wind Speed'])
        else:
            df = pd.DataFrame(columns=['Date', 'Avg Temperature', 'Avg Humidity', 'Avg Wind Speed'])

        # Zapisz DataFrame do pliku CSV
        df.to_csv('202201.csv', index=False)

        print('Dane zostały zapisane do 202201.csv')
    finally:
        driver.quit()
