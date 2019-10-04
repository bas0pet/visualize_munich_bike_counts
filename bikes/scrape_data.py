"""Use python to download data from "https://www.opengov-muenchen.de" licensed with: "Datenquelle: dl-de/by-2-0:
Landeshauptstadt München – Kommunalreferat – GeodatenService – www.geodatenservice-muenchen.de"
"""
import os
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

BASEURL = "https://www.opengov-muenchen.de"
DATAPATH = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'data')
os.makedirs(DATAPATH, exist_ok=True)


def search_open_data_portal(url, maximum_walk=10):
    """Searches sub urls of any page on  "https://www.opengov-muenchen.de" to get urls for downloadable data.

    Parameters
    ----------
    url : str
    maximum_walk : int
        How many pages to walk through

    Returns
    -------

    """
    links_to_open = []
    for page_nr in range(1, maximum_walk):
        soup = visit_homepage(url + f'&page={page_nr}')

        datasets_list = soup.find_all(class_='dataset-content')
        for dataset in datasets_list:
            links_to_open.append(BASEURL + dataset.find('a')['href'])
    return links_to_open


def visit_homepage(url):
    """Requests a given url and returns a BeautifulSoup object.

    Parameters
    ----------
    url : str

    Returns
    -------
    BeautifulSoup object
    """
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_downloadable_data(url_list):
    """Gets all urls where data can be downloaded from.

    Parameters
    ----------
    url_list : list
        List of urls, where to search for downloadable data.

    Returns
    -------
    downloadable_data_list : list
        Direct list of data download urls.
    """
    downloadable_data_list = []
    for url in url_list:
        soup = visit_homepage(url)
        for link in soup.find_all(class_='resource-url-analytics'):
            downloadable_data_list.append(link['href'])
    return downloadable_data_list


def download_data(url_list):
    """Download data from the given url. Works for "https://www.opengov-muenchen.de".
    Stores the data to the local file system

    Parameters
    ----------
    url_list : list
    """
    for URL in url_list:
        url_file = URL.split('/')[-1]
        save_path = os.path.join(DATAPATH, url_file)
        if not os.path.exists(save_path):
            print(f'Download: {URL}')
            urlretrieve(URL, save_path)
        else:
            print(f'Already existing file: -> Skipping: {URL}')
