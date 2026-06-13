'''目标2：自动抓取前5页的所有名言，并处理没有下一页的情况。'''
import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://quotes.toscrape.com'

def get_soup(url):
    """获取一个网址的HTML，返回BeautifulSoup对象"""
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

def get_quotes_from_page(soup):
    """从一页的soup中提取所有名言和作者，返回一个列表"""
    quotes = []
    for quote_div in soup.find_all('div', class_='quote'):
        text = quote_div.find('span', class_='text').text
        author = quote_div.find('small', class_='author').text
        quotes.append((text, author))
    return quotes

def get_next_page_url(soup):
    """从一页的soup中找到'Next'按钮的链接，如果没有则返回None"""
    # 提示：找那个 class="next" 的li标签里的a标签的'href'属性
    next_block = soup.find('a' , class_='next')
    if next_block:
        next_url = next_block.href
    else:
        next_url = None
    return next_url
    pass

# 主程序：循环爬取
current_url = BASE_URL + '/'
all_quotes = []
page_count = 0

while current_url and page_count < 5:  # 限制最多抓5页，防止无限循环
    print(f'正在抓取: {current_url}')
    soup = get_soup(current_url)
    
    # 抓取本页的名言
    all_quotes.extend(get_quotes_from_page(soup))
    
    # 找下一页
    next_page = get_next_page_url(soup)
    if next_page:
        current_url = BASE_URL + next_page  # 拼接完整网址
    else:
        current_url = None  # 没有下一页，结束循环
    page_count += 1

print(f'总共抓到 {len(all_quotes)} 条名言')
# 打印前3条看看
for i, (text, author) in enumerate(all_quotes[:3]):
    print(f'{i+1}. "{text}" — {author}')