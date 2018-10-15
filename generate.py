#!/usr/bin/env python
from jinja2 import Environment, PackageLoader, select_autoescape
import strictyaml
from strictyaml import Map, MapPattern, Url, Bool, Regex
from datetime import datetime


def load_data(filename):
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
    with open(filename) as f:
        return strictyaml.load(f.read(), schema).data


def linkify(text):
    return text.lower().replace(' ', '-').replace('.', '')


def render_j2(data, output_file='index.md'):
    env = Environment(
        loader=PackageLoader(__name__, '.'),
        autoescape=select_autoescape([])
    )
    env.filters['linkify'] = linkify
    templ = env.select_template(['index.j2'])
    return templ.render(
        data=data.items(),
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


if __name__ == '__main__':
    data = load_data('tools.yml')
    with open('index.md', 'w') as f:
        f.write(render_j2(data))
