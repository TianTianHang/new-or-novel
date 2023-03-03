from time import sleep

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.webdriver import WebDriver

url = 'https://twitter.com/search?q={}&src={}&f={}'
xpath = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/section/div/div/div/div/div/article/div/div/div[2]/div[2]'


def init():
    # 设置Chrome的参数，隐藏某些窗口，
    chrome_options = webdriver.ChromeOptions()
    # 无界面浏览器
    chrome_options.add_argument('headless')
    chrome_options.add_argument(
        '--user-agent=' + 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1660.14')
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.capabilities['pageLoadStrategy'] = 'eager'
    chrome_options.add_experimental_option("prefs",
                                           {"profile.password_manager_enabled": False,
                                            "credentials_enable_service": False})
    # chrome驱动路径
    driver_path = '.\\chromedriver\\chromedriver.exe'
    chrome = webdriver.Chrome(options=chrome_options, executable_path=driver_path)
    return chrome


def get_html(chrome: WebDriver, param):
    chrome.get(url.format(param['q'], param['src'], param['f']))
    sleep(20)
    print("开始划动")
    old_height = 400
    new_height = chrome.execute_script('var q=document.body.scrollHeight;return(q)')
    spa = 600
    tweet_set = set()
    try:
        while True:
            for i in range(old_height, new_height, spa):
                chrome.execute_script('window.scrollTo(0,{})'.format(i))
                old_height = i
                try:
                    texts = [t.text for t in chrome.find_elements_by_xpath(xpath)]
                    print(len(texts))
                    for k in texts:
                        tweet_set.add(k)
                except StaleElementReferenceException as e:
                    print("元素丢失")
                sleep(1)
            print("现在有{}条".format(len(tweet_set)))
            if new_height < chrome.execute_script('var q=document.body.scrollHeight;return(q)'):
                new_height = chrome.execute_script('var q=document.body.scrollHeight;return(q)')
            else:
                break
    finally:
        return tweet_set


def write_data(set, path, param):
    df = pd.DataFrame(columns=['text'], data=set)
    df.to_json(path.format(param['word'], param['f']), orient='columns')


if __name__ == '__main__':
    param = {
        'word': 'novel',
        'q': 'novel lang:en',
        'src': 'typed_query',
        'f': 'live'
    }
    chrome = init()
    set1 = get_html(chrome, param)
    write_data(set1, path='.\\twitter-{}-{}.json', param=param)
