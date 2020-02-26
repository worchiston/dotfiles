#!/usr/bin/env python

import sys
import xml.etree.ElementTree as et
from yattag import Doc
from w3lib.html import replace_entities
import html2text


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: %s [blogger XML file]' % sys.argv[0])
        sys.exit()

    try:
        xml = et.iterparse(sys.argv[1])
    except:
        print('Couldn\'t load XML file. Does it exist?')
        sys.exit()
    
    # Strip stupid namespaces
    for _, node in xml:
        if '}' in node.tag: node.tag = node.tag.split('}', 1)[1]

    root = xml.root

    # Actual entries (not settings) have a '*.post-*' in the <id>. Skip if not present
    entries = [entry for entry in root.findall('entry') if '.post-' in entry.find('id').text]

    # Setup yattag/HTML stuff
    doc, tag, text, line = Doc().ttl()
    
    # Entries to HTML
    doc.asis('<!DOCTYPE html>')
    with tag('html', 'lang="en"'):
        with tag('head'):
            doc.stag('meta charset="utf-8"')
            with tag('title'): text('blogger2html OUTPUT')
        with tag('body'):
            for entry in entries:
                with tag('article'):
                    with tag('h1'): text(entry.find('title').text)
                    with tag('h4'): text('Published: {}'.format(entry.find('published').text))
                    with tag('h4'): text('Updated: {}'.format(entry.find('updated').text))
                    with tag('code'): text(html2text.html2text(entry.find('content').text))
                doc.stag('hr')

    # HTML to file
    with open('output.html', 'w') as fd:
        fd.write(doc.getvalue().encode('utf-8'))
