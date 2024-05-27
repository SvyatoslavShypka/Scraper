import requests
import requests_html

# scrapper for the main real project

# URL strony do pobrania danych
URL = "https://www.wunderground.com/history/monthly/pl/wroc%C5%82aw/EPWR/date/2023-1"
page = requests.get(URL)

# Sprawdzenie, czy strona została pobrana pomyślnie
if page.status_code == 200:
    # Zapisanie zawartości strony do pliku html
    with open('page_content.html', 'w', encoding='utf-8') as file:
        file.write(page.text)

    print('Zawartość strony została zapisana do pliku page_content.html')
else:
    print(f'Nie udało się pobrać strony. Kod statusu: {page.status_code}')
