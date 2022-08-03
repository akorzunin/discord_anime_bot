from tinydb import TinyDB

db = TinyDB('./data/db.json')

souds = db.table('souds')
stickers = db.table('stickers')
