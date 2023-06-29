import functools

import requests
from sqlalchemy import func

from models import WordList
from sqlalchemy import and_


def add_kw(db, kw_info):
    s = db.session
    wordList = dict_to_wordlist(kw_info)
    s.add(wordList)
    s.commit()
    return wordList.id


def update_kw(db, kw_info):
    s = db.session
    wordList = dict(pre_words=kw_info['word']['pre_words'],
                    post_words=kw_info['word']['post_words'],
                    title=kw_info['title'],
                    content=kw_info['content'],
                    parent_id=kw_info['parent_id'],
                    has_hover=kw_info['has_hover'], )
    rs = s.query(WordList).filter_by(id=kw_info['id']) \
        .update(wordList)
    s.commit()
    return rs


def remove_kw(db, kw_id):
    s = db.session
    rs = s.query(WordList).filter_by(id=kw_id).delete()
    s.commit()
    return rs



def get_kw_by_id(db, kw_id):
    s = db.session
    kw = s.query(WordList).filter(and_(WordList.id == kw_id, WordList.parent_id != None)).all()
    if len(kw) != 0:
        return wordlist_to_dict(*kw)
    return {}


def get_tree(db):
    tree = []
    s = db.session
    roots = s.query(WordList).filter(WordList.parent_id == None).all()
    for root in roots:
        root_dict = wordlist_to_dict(root)
        root_dict["children"] = get_children(root)
        tree.append(root_dict)
    return tree


def get_children(wordlist):
    children = []
    for child in wordlist.children:
        child_dict = wordlist_to_dict(child)
        child_dict["children"] = get_children(child)
        children.append(child_dict)
    return children


def wordlist_to_dict(wordlist):
    return {
        "id": wordlist.id,
        "word": {
            "pre_words": wordlist.pre_words,
            "post_words": wordlist.post_words,
        },
        "title": wordlist.title,
        "content": wordlist.content,
        "has_hover": wordlist.has_hover
    }


def dict_to_wordlist(wordlist_dict):
    return WordList(pre_words=wordlist_dict['word']['pre_words'],
                    post_words=wordlist_dict['word']['post_words'],
                    title=wordlist_dict['title'],
                    content=wordlist_dict['content'],
                    parent_id=wordlist_dict['parent_id'],
                    has_hover=wordlist_dict['has_hover'], )


# 动态请求bing api接口
@functools.lru_cache(maxsize=1)
def getmapsource():
    bing_map_token = 'AlokyiLvd54vljDRnjUfkF_STJ2nGNZ9N1j_FAFtAMERXrTc57hJdKRyq6yc2EDk'
    req = requests.get('https://dev.virtualearth.net/REST/V1/Imagery/Metadata/CanvasLight?output=json&include'
                       '=ImageryProviders&uriScheme=https&key={BingMapsKey}'.format(BingMapsKey=bing_map_token))
    url_json = req.json()['resourceSets'][0]['resources'][0]
    sources = [url_json['imageUrl'].replace('{subdomain}', sub) for sub in
               url_json['imageUrlSubdomains']]
    return sources
