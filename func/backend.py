import random
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
    
    if not res.text:
        return None
    return res.json()

def get_feed_rand(uuid):
    res = requests.get(urljoin(HOST, '/rand/'))
    logger.info(res.url)

    return res.json()

def get_ans(payload):
    res = requests.post(urljoin(HOST, '/answers/'), data=payload)
    logger.info(res.url)

    if res.status_code == 409:
        return "Error"

    return res.json()['correct']

def get_provoke(correctness):
    res = requests.get(urljoin(HOST, '/provokes/?correct={}'.format(correctness)))
    res_dict = res.json()
    index = random.randint(0, len(res_dict)-1)
    logger.info(res.url)

    return res_dict[index]['message']

def get_status(uuid):
    res = requests.get(urljoin(HOST, '/players/{}/'.format(uuid)))
    logger.info(res.url)
    
    return res.json()
