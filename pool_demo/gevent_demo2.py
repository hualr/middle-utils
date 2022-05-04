import gevent
from bs4 import BeautifulSoup
from gevent import monkey

monkey.patch_all()
import requests


def get_page_source(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title_list = soup.find('div', attrs={'id': 'post_list'}).find_all('a', attrs={'class': 'post-item-title'})
    for title in title_list:
        print(title['href'], title.text)


if __name__ == '__main__':
    threads = []
    for i in range(1, 10):
        page = f'https://www.cnblogs.com/#p{i}'
        threads.append(gevent.spawn(get_page_source, page))
    gevent.joinall(threads)
