import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to extract movie data from an HTML table
def get_movies_from_table(table):
    """
    Extracts movie data from an HTML table on a web page.

    Args:
        table (BeautifulSoup Tag): The HTML table tag.

    Returns:
        list: A list of dictionaries containing movie data.
    """
    return [
        {
            'name': columns[0].text.strip(),     # Extract the movie name from the first column
            'release_date': columns[1].text.strip()  # Extract the release date from the second column
        }
        for row in table.find_all('tr')[1:]     # Iterate through the rows in the table, excluding the header row
        for columns in [row.find_all('td')]     # Find all data columns in a row
        if len(columns) >= 2  # Check if there are at least 2 data columns in a row
    ]

# Main function to retrieve movie data
def get_movies(url):
    """
    Retrieves movie data from a web page and its related pages.

    Args:
        url (str): The URL of the web page.

    Returns:
        list: A list of dictionaries containing movie data.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table', {'class': 'wikitable'})  # Find all tables with the 'wikitable' class

    movies = [movie for table in tables for movie in get_movies_from_table(table)]

    return movies

def main():
    # URL of the main page
    base_url = "https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films"
    movies = get_movies(base_url)

    # Check if there are additional pages for more recent movies
    next_pages = [link['href'] for link in soup.find_all('a', href=True)
                  if "List_of_Walt_Disney_Pictures_films_from_1960" in link['href']]

    for next_page_url in next_pages:
        next_page_movies = get_movies("https://en.wikipedia.org" + next_page_url)
        movies.extend(next_page_movies)  # Add movies from the current page to the list

    # Convert the list of dictionaries into a Pandas DataFrame
    df = pd.DataFrame(movies)

    # Save the DataFrame to an Excel file
    df.to_excel('disney_movies.xlsx', index=False, engine='openpyxl')  # Export the data to an Excel file

if __name__ == "__main__":
    main()