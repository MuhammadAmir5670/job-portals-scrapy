from scraper.portals import weworkremotely as wwr
from scraper.portals import dice
from scraper.portals import builtin
from scraper.portals import simplyhired
from scraper.portals import remoteok

PORTALS = {"weworkremotely": wwr.weworkremotely, "dice": dice.dice,
           "builtin": builtin.builtin, "simplyhired": simplyhired.simplyhired, "remoteok":remoteok.remoteok}
