import logging
import requests
import json
from random import choice

class AnimePicture(object):
    def __init__(self, *args, **kwargs):
        super(AnimePicture, self).__init__(*args)
        self.type_ = kwargs.pop('type', 'sfw')
        self.categories = kwargs.pop('categories', ['waifu'])
    def get_url(self, category_=None):
        category = choice(self.categories) if category_ is None else category_
        endpoint = f'https://api.waifu.pics/{self.type_}/{category}'
        r = requests.get(endpoint)
        loaded_json = json.loads(r.text)

        return loaded_json['url']
    def get_urls(self, amount: int, *args, **kwrags):
        category = kwrags.pop('category', 'waifu')
        endpoint = f'https://api.waifu.pics/many/{self.type_}/{category}'
        data = {
            "files": 0
        }
        r = requests.post(endpoint, data)
        loaded_json = json.loads(r.text)
        urls = loaded_json['files']
        return urls[:amount]
    def get_azure(self,  data, *args, **kwrags):
        args = data
        try:
            name = args[0]
        except IndexError: name = 'random'
        if name == 'random':
            url = 'https://formidable.kashima.moe/ships/random'
        elif name == 'id':
            try:
                id = int(args[1])
            except ValueError: return
            url = f'https://formidable.kashima.moe/ships/id?code={args[1]}'
        elif name == 'name':
            try:
                url_name = '+'.join(args[1:])
                url = f'https://formidable.kashima.moe/ships/class?name={url_name}'
                r = requests.get(url, )
                data =r.json()
                if len(data) == 0: 
                    logging.debug(0)
                    return 0
                s = data['skins']
                return s
            except TypeError: logging.debug('s1 failed to parse')
            try:
                url_name = '+'.join(args[1:])
                url = f'https://formidable.kashima.moe/ships/class?name={url_name}'
                r = requests.get(url, )
                data =r.json()
                if len(data) == 0: 
                    logging.debug(0)
                    return 0
                return data[0]['skins']
            except TypeError: logging.debug('s2 failed to parse')

        r = requests.get(url, )
        data =r.json()
        if len(data) == 0: 
            logging.debug(0)
            return 0
        s = data['skins']
        return s
        


if __name__ == '__main__':
    a = AnimePicture()
    print(a.get_url())
    print(a.get_urls(10, category='neko'))
    
