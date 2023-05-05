import requests
from sqlalchemy import func

from utils.models import WordList


def get_tree(db):
    tree = []
    s = db.session
    roots = s.query(WordList).filter(WordList.parent_id == None).all()
    for root in roots:
        root_dict = wordlist_to_dict(root)
        root_dict["children"] = get_children(root)
        tree.append(root_dict)
    nextId = s.query(func.max(WordList.id)).scalar()
    return tree, nextId


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
        "img": wordlist.img,
        "has_hover": wordlist.has_hover
    }


def getmessage(request):
    json_data = request.get_json()
    timeframe_list = json_data['timeframe_list']
    kw_list = json_data['kw_list']
    title = json_data['title']
    timeframe_list_c = []
    for timeframe in timeframe_list:
        timeframe_list_c.append(timeframe[0] + ' ' + timeframe[1])
    return kw_list, timeframe_list_c, title


def getmapsource():
    bing_map_token = 'AlokyiLvd54vljDRnjUfkF_STJ2nGNZ9N1j_FAFtAMERXrTc57hJdKRyq6yc2EDk'
    # uriScheme=https 请求到的url协议改为https（https和http不能混用）
    req = requests.get('https://dev.virtualearth.net/REST/V1/Imagery/Metadata/CanvasLight?output=json&include'
                       '=ImageryProviders&uriScheme=https&key={BingMapsKey}'.format(BingMapsKey=bing_map_token))
    url_json = req.json()['resourceSets'][0]['resources'][0]
    sources = [url_json['imageUrl'].replace('{subdomain}', sub) for sub in
               url_json['imageUrlSubdomains']]
    return sources
