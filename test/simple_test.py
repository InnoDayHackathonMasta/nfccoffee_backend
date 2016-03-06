from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import coffeeapp
import unittest

class CoffeeAppTestCase(unittest.TestCase):

    def setUp(self):
        coffeeapp.app.config['TESTING'] = True
        self.app = coffeeapp.app.test_client()

    def tearDown(self):
        pass

    def test_simple(self):
        rv = self.app.get('/')
        assert 'hello world!' in rv.data

if __name__ == '__main__':
    unittest.main()
