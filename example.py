from urllib.request import urlopen
from bs4 import BeautifulSoup
from pandas import DataFrame

def clean_element_text(element):
    # Clean and return the text from the element
    base = element.text.strip()
    try:
        return float(base)
    except ValueError:
        return base

def find_parent_table(soup):    
    # Find the parent of the table
    return soup.find('div', {"class": "content"})

def find_header_row(parent_table):
    # Find the header row of the table
    return parent_table.find('div', {"class": "titlebox"})

def find_header_columns(header_row):
    # Find all the columns in the header row
    return header_row.findAll('div', {"class": ["lis_insider", "lis_insider4"]})

def find_all_data_rows(parent_table):
    # Find all the rows in the parent table
    return parent_table.findAll('div', {"class": "t_box"})

def find_all_data_columns(data_row):
    # Find all the columns in this row
    return data_row.findAll('div', {"class": ["lis_box_insider", "lis_box_insider4"]})

def main(url):
    """ Loads the given URL and then uses the above rules to find and process the data table.

    Args:
        url (str): The webpage containing the data table.

    Returns:
        DataFrame: DataFrame containing the extracted data.
    """

    # Load a webpage from a URL and then create a BeautifulSoup object from the contents
    with urlopen(url) as webobj:
        soup = BeautifulSoup(webobj.read(), 'html.parser')

    # Find the parent table
    parent_table = find_parent_table(soup)

    # We can create the headers in one step
    headers = [ clean_element_text(col)
        for col in find_header_columns(find_header_row(parent_table)) ]

    # Create the DataFrame in more step
    df = DataFrame([
            [ clean_element_text(col) for col in find_all_data_columns(row) ]
            for row in find_all_data_rows(parent_table) ],
        columns=headers)

    # Use dropna to do a final cleanup
    return df.dropna()

if __name__ == "__main__":
    url = "http://www.scrapregister.com/scrap-prices/united-states/260"
    df = main(url)
    print(df)
    df.to_csv("scrap-prices.csv")
