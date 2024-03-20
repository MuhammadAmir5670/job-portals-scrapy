from scraper.portals import weworkremotely as wwr
from scraper.portals import dice
from scraper.portals import builtin
from scraper.portals import simplyhired
from scraper.portals import remoteok
from scraper.portals import ziprecruiter

PORTALS = {
    "weworkremotely": wwr.weworkremotely,
    "dice": dice.dice,
    "builtin": builtin.builtin,
    "ziprecruiter": ziprecruiter.ziprecruiter,
    "simplyhired": simplyhired.simplyhired,
    "remoteok":remoteok.remoteok
}
