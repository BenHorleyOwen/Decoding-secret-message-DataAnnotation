#im writing this in the prefered language, java or C++ also works for me
#considering its a plaintext unicode document with only a URL provided; i dont need an API key
# this is written assuming only one table is present
import requests
from bs4 import BeautifulSoup

#functions
def documentRetrieval(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else: 
        return "failed to retrieve"


def printGrid(data):
    max_x = max(item['x'] for item in data)
    max_y = max(item['y'] for item in data)
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for item in data:
        x, y, char = item['x'], item['y'], item['char']
        grid[y][x] = char  # Note: y is row, x is column

    for row in reversed(grid): #the y coords are given upsidedown, hence the rows are printed backwards
        print(''.join(row))

def parseTable(table):
    data = []
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        x = int(cells[0].get_text(strip=True))
        char = cells[1].get_text(strip=True)
        y = int(cells[2].get_text(strip=True))
        data.append({'x': x, 'char': char, 'y': y})
    return data

        
documentURL = "https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub"
soup = BeautifulSoup(documentRetrieval(documentURL), 'html.parser')
printGrid(parseTable(soup.find('table')))
