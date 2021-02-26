import requests
from .config import HOST
from .logger import logger
from urllib.parse import urljoin

def register(payload):
    res = requests.post(urljoin(HOST, '/players/'), json=payload)
    logger.info(res.url)

    if not res.ok:
        return

    return res.json()

def seacher(u_id):
    res = requests.get(urljoin(HOST, '/mappings/{}'.format(u_id)))
    logger.info(res.url)
   
    if res.status_code == 404:
        return

    return res.json()

def get_feed(uuid):
    res = requests.get(urljoin(HOST, '/feeds/{}'.format(uuid)))
    logger.info(res.url)

    return res.json()

def get_feed_rand(uuid):
    res = requests.get(urljoin(HOST, '/rand/'))
    logger.info(res.url)

    return res.json()

def get_ans(payload):
    res = requests.post(urljoin(HOST, '/answers/'), data=payload)
    correctness = res.json()['correct']
    logger.info(res.url)

    if res.status_code == 409 and correctness:
        return "error"

    return correctness

def get_provoke(correctness):
    res = requests.get(urljoin(HOST, '/provokes/?correct={}'.format(correctness)))
    logger.info(res.url)
    
    return res.json()[0]['message']

def get_status(uuid):
    res = requests.get(urljoin(HOST, '/players/{}/'.format(uuid)))
    logger.info(res.url)
    
    return res.json()
