from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

def get_all_quotes():
    conn = sqlite3.connect('quotes.db')
    c = conn.cursor()
    c.execute('SELECT text, author FROM quotes')
    data = c.fetchall()
    conn.close()
    return data

def get_author_ranking():
    conn = sqlite3.connect('quotes.db')
    c = conn.cursor()
    c.execute('SELECT author, COUNT(*) as cnt FROM quotes GROUP BY author ORDER BY cnt DESC')
    data = c.fetchall()
    conn.close()
    return data

# 用最简单的内联HTML模板
HTML_TEMPLATE = '''
<h1>名人名言档案</h1>
<h2>作者排行榜（按名言数量）</h2>
<ol>
{% for author, cnt in ranking %}
    <li>{{ author }}: {{ cnt }}条</li>
{% endfor %}
</ol>
<h2>最新抓取的名言（前20条）</h2>
<ul>
{% for text, author in quotes[:20] %}
    <li>"{{ text }}" — <strong>{{ author }}</strong></li>
{% endfor %}
</ul>
'''

@app.route('/')
def index():
    quotes = get_all_quotes()
    ranking = get_author_ranking()
    return render_template_string(HTML_TEMPLATE, quotes=quotes, ranking=ranking)

if __name__ == '__main__':
    app.run(debug=True)