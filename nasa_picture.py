from typing import Tuple
import requests

class NasaPicture(object): 
    '''docstring for NasaPicture'''
    def __init__(self, ):
        super(NasaPicture, self).__init__()
        self.API_KEY = 'j7rY3hXtRpXWrsRcZaAtUaMltg7QNlvRA85OmbVQ'

    def get_url(self) -> Tuple[str, str, str]:
        r = requests.get(url=f'https://api.nasa.gov/planetary/apod?api_key={self.API_KEY}')
        url = r.json()['hdurl']
        title = r.json()['title']
        explanation = r.json()['explanation']

        return url, title, explanation


if __name__ == '__main__':
    n = NasaPicture()
    print(n.get_url())