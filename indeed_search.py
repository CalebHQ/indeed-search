import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# application variables
what = input('Job title, keywords, or company: ')
where = input('City, state/territory or postcode: ')


def get_url(position, location):
    '''Generate a URL based on Position and Location'''
    temp = f'https://au.indeed.com/jobs?q={position}&l={location}'
    return temp


def get_record(card):
    '''Extract job data'''
    atag = card.h2.a
    title = atag.get('title')
    url = 'https://au.indeed.com' + atag.get('href')

    company = card.find('span', 'company').text.strip()
    location = card.find('div', 'recJobLoc').get('data-rc-loc')
    summary = card.find('div', 'summary').text.strip()
    postdate = card.find('span', 'date').text.strip()
    today = datetime.today().strftime('%Y-%m-%d')
    try:
        salary = card.find('span', 'salaryText').text.strip()
    except AttributeError:
        salary = ''

    record = (title, company, location, postdate, today, summary, salary, url)

    return record


def main(positon, location):
    '''main program routine'''
    records = []
    url = get_url(what, where)

    # extract job data
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', 'jobsearch-SerpJobCard')

        for card in cards:
            record = get_record(card)
            records.append(record)

        # navigating next page
        try:
            url = 'https://au.indeed.com' + \
                soup.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            break

    # saving the data
    with open('indeed_results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['JobTitle', 'Company', 'Location', 'PostDate',
                         'ExtractDate', 'Summary', 'Salary', 'JobUrl'])
        writer.writerows(records)


# run main program
main(what, where)
print(f'''
Results have been found!
csv file has been created!
''')
