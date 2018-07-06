#!/usr/bin/env python
import markdown_generator as mdg
import json

from jsonschema import validate
import unittest
import httplib2


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
            resp = h.request(tool['Link'], 'HEAD')
            self.assertLess(int(resp[0]['status']), 400)


def get_tool_table_entry(tool):
    def format_data(k, v):
        if k == 'Free':
            return 'Yes' if v else 'No'
        if k == 'Link':
            return mdg.link(v, 'Go')
        return v

    return [
        format_data(k, tool[k])
        for k in ['Title', 'Description', 'Free', 'Link']
    ]


if __name__ == '__main__':
    data = sorted(data.items())

    with open('index.md', 'w') as f:
        writer = mdg.Writer(f)
        writer.writeline('# Tools')
        writer.writeline()

        writer.writeline('## Table of Contents')
        for category, _ in data:
            url = category.lower()
            url = url.replace(' ', '-')
            url = url.replace('.', '')
            url = '#' + url
            writer.writeline('- ' + mdg.link(url, category))

        for category, tools in data:
            writer.writeline()
            writer.writeline('## ' + category)
            writer.writeline()
            table = mdg.Table()
            table.add_column('Title')
            table.add_column('Description')
            table.add_column('Free', mdg.Alignment.CENTER)
            table.add_column('Link')
            for tool in sorted(tools, key=lambda t: t['Title']):
                table.append(*get_tool_table_entry(tool))
            writer.write(table)
