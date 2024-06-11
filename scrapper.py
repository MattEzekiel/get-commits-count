import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_contribution_count(username, year):
    url = f'https://github.com/{username}?tab=overview&from={year}-01-01&to={year}-12-31'
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses

    soup = BeautifulSoup(response.text, 'html.parser')
    contribution_header = soup.select_one('.js-yearly-contributions h2')

    if contribution_header:
        contribution_text = contribution_header.get_text(strip=True)
        contribution_count = int(contribution_text.split(' ')[0].replace(',', ''))
        return contribution_count

    return 0

def main():
    username = 'MattEzekiel'
    current_year = datetime.now().year
    total_contributions = 0

    for year in range(2019, current_year + 1):
        contributions = get_contribution_count(username, year)
        total_contributions += contributions

    print(total_contributions)
    return total_contributions

if __name__ == '__main__':
    main()
