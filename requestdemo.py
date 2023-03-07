import requests
from lxml import etree


def main():
    url = 'https://twitter.com/search'
    testurl = 'https://httpbin.org/get'

    header = {
        'sec-ch-ua': '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1660.14'
    }
    param = {
        'q': 'novel',
        'src': 'typed_query',
        'f': 'top'
    }
    data = {
        'offset': 10
    }
    xml = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/section/div/div/div[{}]/div/div/article/div/div/div[2]/div[2]/div[2]/div/span[1]'
    # response = requests.get(url=url, params=canshu, headers=header, )
    response = requests.get(url=url, headers=header, params=param)
    tree = etree.HTML(response.text)
    with open("test.html", "w", encoding='utf-8') as f:
        for i in range(2, 20):
            text = tree.xpath(xml.format(i * 3))
            f.write(text)


if __name__ == '__main__':
    main()
