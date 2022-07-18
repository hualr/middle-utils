from selenium import webdriver

browser = webdriver.Chrome()

if __name__ == '__main__':
    browser.get('http://www.baidu.com/')
