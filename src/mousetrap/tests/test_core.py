from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import unittest
from mousetrap.core import Loop, Observable


class test_Observable(unittest.TestCase):

    def setUp(self):
        self.observable = Observable()
        self.client1 = Client()
        self.client2 = Client()

    def test_observable_callback_noArguments_success(self):
        self.observable.subscribe(self.client1)
        self.observable._fire('callback')
        self.assertTrue(
                len(self.client1.callback_params) == 1,
                msg="callback not called."
                )

    def test_observable_callback_withArguments_success(self):
        self.observable._add_argument('param', 'param')
        self.observable.subscribe(self.client1)
        self.observable._fire('callback')
        self.assertEquals(
                'param', self.client1.callback_params[0]['param'],
                msg="param not passed correctly."
                )

    def test_multiple_subscribers(self):
        self.observable.subscribe(self.client1)
        self.observable.subscribe(self.client2)
        self.observable._fire('callback')
        self.assertTrue(
                len(self.client1.callback_params) == 1,
                msg="callback not called on client1."
                )
        self.assertTrue(
                len(self.client2.callback_params) == 1,
                msg="callback not called on client2."
                )


class Client(object):
    def __init__(self):
        self.callback_params = []

    def callback(self, param=None):
        self.callback_params.append({'param':param})



class test_Loop(unittest.TestCase):

    def setUp(self):
        self.config = {'loops_per_second': 10}
        self.loop = Loop(self.config, app=None)

    def test_loop(self):
        self.loop.start()


if __name__ == '__main__':
    unittest.main()
