from typing import Tuple
import requests

class NasaPicture(object): 
    '''docstring for NasaPicture'''
    def __init__(self, ):
        super(NasaPicture, self).__init__()
        self.API_KEY = 'j7rY3hXtRpXWrsRcZaAtUaMltg7QNlvRA85OmbVQ'

    def get_url(self) -> Tuple[str, str, str, str, str]:
        r = requests.get(url=f'https://api.nasa.gov/planetary/apod?api_key={self.API_KEY}')
        try:
            url = r.json()['hdurl']
        except KeyError:
            url = r.json()['url']
        title = r.json()['title']
        text_data = r.json()['explanation']
        explanation = ''.join(text_data.split('. ')[:-1])+'.'
        stat = ''.join(text_data.split('. ')[-1].split(': ')[0])+':'
        try:
            stat_value = ''.join(text_data.split('. ')[-1].split(': ')[1])
        except IndexError: stat_value = ''
        return url, title, explanation, stat, stat_value


if __name__ == '__main__':
    n = NasaPicture()
    print(n.get_url())