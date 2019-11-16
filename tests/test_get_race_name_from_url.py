from unittest import TestCase


class TestGet_race_name_from_url(TestCase):
    def test_get_race_name_from_url(self):
        get_race_name_from_url('en/results/6-ironman-703-zell-am-see/all/')
        get_race_id_from_url('en/results/6-ironman-703-zell-am-see/all/')

