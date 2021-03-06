import logging
import requests
import yaml

import os
PWD = os.path.abspath(os.getcwd())

class GachiHandler(object): 
    '''docstring for ClassName'''
    def __init__(self, *args):
        super(GachiHandler, self).__init__()
        with open(os.path.join(PWD, 'src', 'static_data', 'gachi_dict.yaml'), 'r') as f: 
            self.r = yaml.load(f, Loader=yaml.FullLoader)


    def validate_gachi(self, query: str) -> str:
        r = self.r
        r_val = []
        r_key = []
        for key, val in r.items():
            if query.lower() in str(key).lower():
                r_val.append(val)
                r_key.append(key)
                logging.debug( f"{val}, {key}")
        return dict(zip(r_key, r_val))

if __name__ == '__main__':
    g = GachiHandler()
    q = g.validate_gachi('sorry for')
    print(len(q))
    import random
    c = random.choice(list(q.items()))
    print(c)
