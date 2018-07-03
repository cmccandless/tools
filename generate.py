#!/usr/bin/env python
import markdown_generator as mdg
import json


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


with open('tools.json') as f:
    data = sorted(json.load(f).items())

with open('index.html', 'w') as f:
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
