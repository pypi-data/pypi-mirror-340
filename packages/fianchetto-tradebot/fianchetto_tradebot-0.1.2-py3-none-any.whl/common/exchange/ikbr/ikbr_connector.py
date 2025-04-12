import configparser
import logging
import os

from common.exchange.connector import Connector

config = configparser.ConfigParser()

DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.ini')
DEFAULT_ETRADE_SESSION_FILE = os.path.join(os.path.dirname(__file__), 'ikbr_session.out')


logger = logging.getLogger(__name__)


class SchwabConnector(Connector):

    def __init__(self, config_file=DEFAULT_CONFIG_FILE, session_file=DEFAULT_ETRADE_SESSION_FILE):
        self.config_file = config_file
        self.session_file = session_file

    def get_exchange(self):
        return "IKBR"


if __name__ == "__main__":
    pass
