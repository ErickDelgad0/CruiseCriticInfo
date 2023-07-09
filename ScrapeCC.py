import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Load previously saved data if available
try:
    df = pd.read_excel('cruise_reviews.xlsx')
    data = df.to_dict('records')
    processed_ports = set(df['Port Name'])
except FileNotFoundError:
    data = []
    processed_ports = set()

# Convert port names to integers
processed_ports = {int(float(port)) for port in processed_ports if isinstance(port, (float, str)) and str(port).isdigit()}

# Loop through portofcall from 2771 to 8888
for portofcall in range(2771, 8888):
    print(" ")
    print(f"--- Port Of Calling: {portofcall} ---")
    # Construct the URL
    url = f"https://www.cruisecritic.com/cruiseto/cruiseitineraries.cfm?portofcall={portofcall}"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the response was successful
    if response.status_code == 200:
        print("found port of call url")
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the reviews URL
        reviews_link = soup.find('a', class_='chakra-link css-szfr4z')
        if reviews_link:
            reviews_url = "https://www.cruisecritic.com" + reviews_link['href']
            # Send a GET request to the reviews URL
            reviews_response = requests.get(reviews_url)
            if reviews_response.status_code == 200:
                print(f"Found Reviews URL {reviews_url}")
                # Parse the reviews HTML content
                reviews_soup = BeautifulSoup(reviews_response.content, 'html.parser')

                # Find the rating and review count
                name_element = reviews_soup.find('h1', class_='chakra-heading css-10u2jqt')
                rating_element = reviews_soup.find('div', class_='css-13zbi8x')

                # Extract the text from the elements
                name = name_element.text if name_element else None
                rating = rating_element.text if rating_element else None

                print(name)
                print(rating)

                # Append the extracted data to the list
                data.append({'Port Name': name, 'Rating': rating})

                # Save the DataFrame to an Excel file
                df = pd.DataFrame(data)
                df.to_excel('cruise_reviews.xlsx', index=False)

    # Add a delay of 1 second before the next request
    time.sleep(1)
