#!/usr/bin/env python
from jinja2 import Environment, PackageLoader, select_autoescape
import json
import strictyaml
from strictyaml import Map, MapPattern, Str, Url, Bool, Regex

import unittest
import httplib2
from http import HTTPStatus

schema = MapPattern(
    Regex(u'[A-Za-z. ]+'),
    MapPattern(
        Regex(u'[A-Za-z\\-. ]+'),
        Map(
            {
                'Description': Regex('.+'),
                'Free': Bool(),
                'Link': Url(),
            },
            Regex(u'.+')
        )
    )
)
with open('tools.yml') as f:
    data = strictyaml.load(f.read(), schema).data


class ToolsTest(unittest.TestCase):
    def test_validate_links(self):
        h = httplib2.Http()
        # for tool in (t for ts in data.values() for t in ts):
        for tool in (t for cts in data.values() for t in cts.values()):
            url = tool['Link']
            resp = h.request(url, 'HEAD')
            status = HTTPStatus(int(resp[0]['status']))
            status_msg = f'{status} {status.name}: {url}'
            self.assertLess(
                status,
                300,
                status_msg
            )


def linkify(text):
    return text.lower().replace(' ', '-').replace('.', '')


def render_j2(data, output_file='index.md'):
    env = Environment(
        loader=PackageLoader(__name__, '.'),
        autoescape=select_autoescape([])
    )
    env.filters['linkify'] = linkify
    templ = env.select_template(['index.j2'])
    return templ.render(data=data.items())


if __name__ == '__main__':
    with open('index.md', 'w') as f:
        f.write(render_j2(data))
