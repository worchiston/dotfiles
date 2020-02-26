#!/usr/bin/python3

import os
import sys
from glob import glob
import sqlite3
from bs4 import BeautifulSoup
import dateutil.parser
import re
import pytz


OUT_FILENAME = 'export.db'


def msg_is_forwarded(msg):
    return msg.select_one('div.body > div.forwarded.body')


def msg_get_type(msg):
    media = msg.select_one('div.body > div.media_wrap')

    if not media:
        return 'TEXT'

    # TODO: More varied media types? (stickers, GIFs, voice messages, etc.)
    #       Problem: exports w/ media excluded have different HTML markup
    return 'MEDIA'


def msg_get_data(prev_dispname, msg):
    msgtype = msg_get_type(msg)
    timestamp = msg.select_one('div.body > div.date')['title']

    # NOTE: Exports do not use ISO 8601 so there's no programmatic way of
    #       detecting timezones (the default depends on that of the exporting
    #       user). But, convert to ISO 8601; AEST
    # TODO: option to convert (-> UTC?) if export's timezone is known
    timestamp = dateutil.parser.parse(timestamp).astimezone().isoformat()

    # Subsequent messages sent by the same user do not have a display name
    # label, hence, one must keep track of the previous display name and use
    # that when necessary
    if 'joined' in msg.attrs['class']:
        dispname = prev_dispname
    else:
        dispname = msg.select_one('div.body > div.from_name').text.strip()

        # Some display names have a stupid 'via @\w+' suffix to be removed
        dispname = re.sub(r'\s*via @\w+$', '', dispname)
        prev_dispname = dispname

    # 'Deleted Account' -> None (NULL) for easier detection
    if dispname == 'Deleted Account':
        dispname = None

    if msgtype != 'TEXT':
        content = None
    else:
        content = msg.select_one('div.body > div.text').text.strip()

    return (msgtype, timestamp, dispname, content)


if __name__ == '__main__':
    if len(sys.argv) is not 2:
        print('Usage: {} [path to export directory]'.format(sys.argv[0]))
        sys.exit()

    if not os.path.isdir(sys.argv[1]):
        print('Path is not a directory.')
        sys.exit()

    filepaths = glob(os.path.join(sys.argv[1], '*.html'))

    # Sort by modification date because glob() does not return paths in
    # ascending order
    filepaths.sort(key=os.path.getmtime)

    outpath = os.path.join(sys.argv[1], OUT_FILENAME)
    db = sqlite3.connect(outpath)
    cur = db.cursor()

    cur.execute('DROP TABLE IF EXISTS export')
    cur.execute('''
        CREATE TABLE export (
            file,
            msgtype,
            timestamp,
            dispname,
            content
        )
    ''')  # Incl. 'file' column for debugging — remove later(?)

    for i, filepath in enumerate(filepaths):
        print('Parsing: {} ({}%)'.format(
            filepath, int(i / len(filepaths) * 100)))

        with open(filepath) as fd:
            soup = BeautifulSoup(fd.read(), features='lxml')

        msgs = soup.find_all('div', {'class': 'message'})
        prev_dispname = None

        for msg in msgs:
            # System/service messages are useless (no timestamps) so skip them
            if 'service' in msg.attrs['class']:
                continue

            if msg_is_forwarded(msg):
                continue

            msgtype, timestamp, dispname, content = msg_get_data(
                prev_dispname, msg)
            prev_dispname = dispname

            cur.execute(
                'INSERT into export VALUES (?, ?, ?, ?, ?)', (
                    os.path.basename(filepath),
                    msgtype,
                    timestamp,
                    dispname,
                    content
                )
            )

        db.commit()

    db.close()

    print('===\nDone. Saved to: ' + outpath)
