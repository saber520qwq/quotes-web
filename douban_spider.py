import requests
from bs4 import BeautifulSoup
import sqlite3
import time

# 1. 伪装成浏览器，绕过最基本的反爬
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_soup(url):
    response = requests.get(url, headers=HEADERS)
    return BeautifulSoup(response.text, 'html.parser')

def crawl_douban_top250():
    all_books = []
    for start_num in range(0, 250, 25):
        url = f'https://book.douban.com/top250?start={start_num}'
        print(f'正在抓取: {url}')
        soup = get_soup(url)
        
        for item in soup.find_all('tr', class_='item'):
            # 提取书名、作者、评分、简介等
            title_div = item.find('div', class_='pl2')
            title = title_div.find('a')['title'] if title_div else '无书名'
            
            author_info = item.find('p', class_='pl')
            author = author_info.text.split('/')[0].strip() if author_info else '无作者'
            
            rating_span = item.find('span', class_='rating_nums')
            rating = rating_span.text if rating_span else '无评分'
            
            quote_span = item.find('span', class_='inq')
            quote = quote_span.text if quote_span else ''
            
            all_books.append((title, author, float(rating) if rating != '无评分' else 0.0, quote))
        
        time.sleep(1) # 礼貌爬虫，避免请求太快被封
    
    return all_books

# 存储到新数据库
conn = sqlite3.connect('books.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        rating REAL,
        quote TEXT
    )
''')
c.execute('DELETE FROM books') # 清空旧数据，避免重复

books = crawl_douban_top250()
c.executemany('INSERT INTO books (title, author, rating, quote) VALUES (?,?,?,?)', books)
conn.commit()
conn.close()
print(f'成功抓取并存储 {len(books)} 本书籍信息')