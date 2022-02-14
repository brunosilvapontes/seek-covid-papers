from os.path import exists
import json

bookmarks_file = 'bookmark.txt'


def persist_bookmark(bookmark_json):
    bookmark_str = json.dumps(bookmark_json)

    if exists(bookmarks_file):
        with open(bookmarks_file, 'r') as f:
            for line in f.read().splitlines():
                if line == bookmark_str:
                    return 'paper already bookmarked'
    
    with open(bookmarks_file, 'a') as f:
        f.write(f'{bookmark_str}\n')
    
    return None


def get_bookmarks_list():
    bookmarks = []

    if not exists(bookmarks_file):
        return []

    with open(bookmarks_file, 'r') as f:
        for line in f.read().splitlines():
            bookmarks.append(json.loads(line))

    return bookmarks
