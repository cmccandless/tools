import unittest
import httplib2
from http import HTTPStatus


from generate import load_data


class ToolsTest(unittest.TestCase):
    def setUp(self):
        self.data = load_data('tools.yml')

    def test_validate_links(self):
        h = httplib2.Http()
        for tool in (t for cts in self.data.values() for t in cts.values()):
            url = tool['Link']
            resp = h.request(url, 'HEAD')
            status = HTTPStatus(int(resp[0]['status']))
            status_msg = f'{status} {status.name}: {url}'
            self.assertLess(
                status,
                300,
                status_msg
            )
