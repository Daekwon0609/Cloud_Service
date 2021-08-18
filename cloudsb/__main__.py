from cloudsb.bot import run
from utils.json import load_j

if token := load_j['token']:
    run(token)