from scraper.portals import weworkremotely as wwr
from scraper.portals import dice
from scraper.portals import builtin
from scraper.portals import simply_hired

PORTALS = {"weworkremotely": wwr.weworkremotely, "dice": dice.dice,
           "builtin": builtin.builtin, "simplyhired": simply_hired.simplyhired}
