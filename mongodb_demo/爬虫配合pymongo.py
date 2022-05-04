import requests
from lxml import etree
# 1、将目标网站抓取下来
from pymongo import MongoClient


def spider_html():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
    }
    url = 'https://movie.douban.com/'
    res = requests.get(url, headers=headers)
    # print(res.text)
    with open('download/douban.html', 'w', encoding='utf-8') as f:
        f.write(res.text)


# 2、提取抓取下来的网站信息
def get_info(source):
    html_element = etree.parse(source, parser=etree.HTMLParser(encoding='utf-8'))
    ul = html_element.xpath('//ul[@class="ui-slide-content"]')[0]
    # print(etree.tostring(ul,encoding='utf-8').decode())
    lis = ul.xpath('.//li[@class="ui-slide-item"]')

    for li in lis:
        try:
            title = li.xpath('./@data-title')[0]  # 标题
            release = li.xpath('./@data-release')[0]  # 发行时间
            rate = li.xpath('./@data-rate')[0]  # 评分
            star = li.xpath('./@data-star')[0]  # 星星
            trailer = li.xpath('./@data-trailer')[0]  # 预告片
            ticket = li.xpath('./@data-ticket')[0]  # 买票网址
            duration = li.xpath('./@data-duration')[0]  # 影片时长
            region = li.xpath('./@data-region')[0]  # 国家地区
            director = li.xpath('./@data-director')[0]  # 导演
            actors = li.xpath('./@data-actors')[0]  # 演员
            rater = li.xpath('./@data-rater')[0]  # 评分人数
            intro = li.xpath('./@data-intro')[0]  # 简介
            enough = li.xpath('./@data-enough')[0]  # 是否有票
            poster = li.xpath('.//li[@class="poster"]//img/@src')[0]  # 海报
            movie = {
                'title': title,
                'release': release,
                'rate': rate,
                'star': star,
                'trailer': trailer,
                'ticket': ticket,
                'duration': duration,
                'region': region,
                'director': director,
                'actors': actors,
                'rater': rater,
                'intro': intro,
                'enough': enough,
                'poster': poster
            }

        except:
            title = ''
        else:
            movies.append(movie)
        # print(etree.tostring(li, encoding='utf-8').decode('utf-8'))
    print(movies)


def add_database(movies):
    myclient = MongoClient(
        host='101.201.67.114',
        username='admin',
        password='123456',
        authSource='admin')
    mydb = myclient['soar']
    mycol = mydb['douban']
    x = mycol.insert_many(movies)  # 输出插入的所有文档对应的 _id 值
    for i in mycol.find():
        print(i)


if __name__ == '__main__':
    spider_html()
    movies = []
    get_info('download/douban.html')
    add_database(movies)
