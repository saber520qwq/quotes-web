import requests
from bs4 import BeautifulSoup

# 1. 用 requests 库，把整个网页的源代码下载下来
url = 'http://quotes.toscrape.com/'
response = requests.get(url)
html_content = response.text

# 2. 用 BeautifulSoup 库，把乱糟糟的源代码解析成容易查找的结构
soup = BeautifulSoup(html_content, 'html.parser')
'''
# 3. 用 soup.find() 找到我们看到的第一个“名言”块
first_quote_div = soup.find('div', class_='quote')

# 4. 在这个块里，找到名言文本和作者
text = first_quote_div.find('span', class_='text').text
author = first_quote_div.find('small', class_='author').text
'''
all_quote_div = soup.find_all("div" , class_="quote")

for block in all_quote_div:
    text = block.find('span' , class_='text').text
    author = block.find('small' , class_='author').text
    print(f'名言: {text}')
    print(f'——{author}\n')
'''
# 5. 打印出来！
print(f'名言: {text}')
print(f'—— {author}')
'''