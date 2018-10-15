#!/usr/bin/env python
from jinja2 import Environment, PackageLoader, select_autoescape
import json

from jsonschema import validate
import unittest
import httplib2
from http import HTTPStatus


with open('tools.json') as f:
    data = json.load(f)


class ToolsTest(unittest.TestCase):
    def test_validate_against_schema(self):
        with open('tools.schema') as f:
            schema = json.load(f)
        validate(data, schema)

    def test_validate_links(self):
        h = httplib2.Http()
        for tool in (t for ts in data.values() for t in ts):
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
