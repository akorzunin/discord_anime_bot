import logging
from static_data.gachi_dict import gachi_dict

class GachiHandler(object): 
    '''docstring for ClassName'''
    def __init__(self, *args):
        self.gach_dict = gachi_dict

    def validate_gachi(self, query: str) -> str:
        r_val = []
        r_key = []
        for key, val in self.gach_dict.items():
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
