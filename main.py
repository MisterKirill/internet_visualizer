import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from pyvis.network import Network
import networkx as nx

FIRST_URL = 'https://wikipedia.org/wiki/ru'
DEPTH = 2


def parse_url(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        print(f'FAIL: {url}')
        return

    source_parsed = urlparse(url)

    results = []

    soup = BeautifulSoup(response.text, 'html.parser')
    for a in soup.find_all('a', href=True):
        new_url = a.get('href')
        parsed_url = urlparse(new_url)

        if parsed_url.netloc == source_parsed.netloc and parsed_url.path == source_parsed.path:
            print(f'SAME: {new_url}')
            continue

        if parsed_url.netloc == '' and parsed_url.scheme == '':
            final_url = f'{source_parsed.scheme}://{source_parsed.netloc}{parsed_url.path}{parsed_url.query}'
        elif parsed_url.scheme == '' and parsed_url.netloc != '':
            final_url = f'{source_parsed.scheme}://{parsed_url.netloc}{parsed_url.path}{parsed_url.query}'
        elif parsed_url.netloc != '' and parsed_url.scheme != '':
            final_url = new_url
        else:
            print(f'BAD: {new_url}')
            continue

        if final_url in results:
            continue

        results.append(final_url)
        print(f'FOUND: {final_url}')

    return results


def parse():
    print(parse_url(FIRST_URL))


def main():
    parse()


if __name__ == '__main__':
    main()
