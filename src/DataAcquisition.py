import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import html5lib

competitions_url = 'https://www.endurance-data.com/en/competitions/'
base_race_url = 'http://www.endurance-data.com/'
header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

def convert_to_seconds(time):
    hours, minutes, secs = time.split(':')
    return int(hours) * 3600 + int(minutes) * 60 + int(secs)


def get_race_name_from_url(url):
    m = re.search(r'(ironman.*)\/all',url)
    return(m[1])

def get_race_id_from_url(url):
    m = re.search(r'(\d{1,3})-ironman',url)
    return(m[1])


def get_races():
    '''

    :return:
    '''
    results_urls = []
    for pg in range(1, 20):
        r = requests.get(f'{competitions_url}{pg}', headers=header)
        soup = BeautifulSoup(r.text)
        for race in soup.find_all('a', class_='btn'):
            href = race['href']
            if re.search('703.*/all', href):
                results_urls.append(href[1:])
    ds = pd.Series(results_urls)
    ds.to_csv('../data/results_urls.txt')


def get_all_race_results(races, write_data=True):
    all_results = []
    for race_url in races:
        results = get_race_results(race_url, write_data)
        all_results.append(results)
    ds_all_results = all_results.pop()
    ds_all_results.append(ds_all_results,ignore_indexes=False)
    if write_data:
        ds_all_results.to_csv("../data/all_results.csv")
    return ds_all_results

def get_race_results(race_url, write_data=True):
    print(f'Currently checking {race_url}')
    more_pages = True
    result_list = []
    results_page = 0
    while (more_pages):
        results_page += 1
        try:
            req_url = f'{base_race_url}{race_url}{results_page}'
            print(req_url)
            r = requests.get(req_url)
            ds_race_results = pd.read_html(r.text, header=0)[0]
            ds_race_results.rename(columns={'Ovr': 'OverallRank',
                                            'Gen': 'GenderRank',
                                            'Div': 'DivRank',
                                            '#': 'Bib',
                                            'AG': 'AgeGroup',
                                            'Unnamed: 6': 'Country',
                                            'Unnamed: 7': "SwimTime",
                                            'Unnamed: 8': 'BikeTime',
                                            'Unnamed: 9': 'RunTime',
                                            'Unnamed: 10': 'Overall'},
                                   inplace=True)
            result_list.append(ds_race_results)
        except ValueError:
            more_pages = False

    ds_results = result_list.pop()
    ds_results = ds_results.append(result_list, ignore_index=True)
    ds_results['Race'] = get_race_name_from_url(race_url)

    if write_data:
        ds_results.to_csv(f'../data/{get_race_id_from_url(race_url)}.csv')

    return ds_results

#get_race_results('en/results/466-ironman-703-xiamen/all/')
get_all_race_results(['en/results/466-ironman-703-xiamen/all/','en/results/373-ironman-703-victoria/all/'])