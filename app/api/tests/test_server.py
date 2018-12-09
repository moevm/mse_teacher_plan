import unittest
from typing import List
from multiprocessing import Process
from time import sleep
import urllib3


def get_page(name: str):
    return f'http://127.0.0.1:5000/{name}'


class ServerTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        from app import app
        self.server = Process(target=app.run)
        self.server.start()
        self.http = urllib3.PoolManager()
        self.waitForConnection()

    def tearDown(self):
        self.server.terminate()

    def waitForConnection(self):
        tries = 0
        max_tries = 10
        while tries < max_tries:
            try:
                self.assertRouteExists('')
                break
            except (ConnectionRefusedError, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError):
                tries = tries + 1
                if tries >= max_tries:
                    self.server.terminate()
                    raise AssertionError('App was not run')
                else:
                    sleep(1)

    def assertRouteExists(self, page: str):
        if self.http.request('GET', get_page(page)).status != 200:
            raise AssertionError(f'Route {get_page(page)} does not exists')

    def assertMultipleRoutesExist(self, routes: List[str]):
        for route in routes:
            self.assertRouteExists(route)

    def test_routes(self):
        self.assertMultipleRoutesExist(['', 'index', 'tpfillbd', 'tpnewplan', 'tpplanlist', 'profile_edit', 'tpprofile',
                                        'login', 'registration', 'tpreport', 'tpuserlist'])

