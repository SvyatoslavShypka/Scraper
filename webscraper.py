import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the weather history page for Wrocław for January 2022
# it does not work properly. Need to use tool which runs JavaScript code and only after that downloads webpage code
url = 'https://www.wunderground.com/history/monthly/pl/wroc%C5%82aw/EPWR/date/2022-1'

# Send a GET request to the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the webpage content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Initialize lists to hold dates and average temperatures
    dates = []
    avg_temps = []

    # Find the table that contains the average temperature data
    table = soup.find('table', {'class': 'days ng-star-inserted'})

    if table:
        # Extract all rows from the table
        rows = table.find_all('tr')

        # Iterate over the rows to find the cells with temperature data
        for row in rows:
            cells = row.find_all('td', class_='ng-star-inserted')
            if len(cells) >= 1:  # Check if the row has the correct number of cells
                # Extract date and temperature
                date_cell = row.find('tr').get_text(strip=True)  # Date is usually in the <th> tag
                avg_temp = cells[0].get_text(strip=True)  # Adjust the index based on the cell position

                # Append the data to lists
                dates.append(date_cell)
                avg_temps.append(avg_temp)

        # Create a DataFrame from the data
        data = pd.DataFrame({
            'Date': dates,
            'Avg Temperature': avg_temps
        })

        # Save DataFrame to CSV
        data.to_csv('avg_temperatures.csv', index=False)

        print('Data has been saved to avg_temperatures.csv')
    else:
        print('Could not find the table with average temperature data.')
else:
    print(f'Failed to retrieve the page. Status code: {response.status_code}')
