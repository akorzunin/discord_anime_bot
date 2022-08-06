from tinydb import TinyDB

db = TinyDB('./data/db.json')

sounds = db.table('sounds')
stickers = db.table('stickers')
