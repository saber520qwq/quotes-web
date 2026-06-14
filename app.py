from flask import Flask, render_template_string, request
import sqlite3
import matplotlib
matplotlib.use('Agg') # 关键：让matplotlib在没有GUI的服务器上也能画图
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row # 让查询结果可以用键名访问
    return conn

def get_all_books():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return books

def search_books(query):
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books WHERE title LIKE ? OR author LIKE ?', 
                         (f'%{query}%', f'%{query}%')).fetchall()
    conn.close()
    return books

def create_rating_histogram():
    conn = get_db_connection()
    ratings = [row['rating'] for row in conn.execute('SELECT rating FROM books').fetchall()]
    conn.close()
    
    plt.figure(figsize=(8, 4))
    plt.hist(ratings, bins=20, color='skyblue', edgecolor='black')
    plt.title('DouBan Top250 Books - Rating Distribution')
    plt.xlabel('Rating')
    plt.ylabel('Number of Books')
    
    # 把图表转成能在网页上显示的base64字符串
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url

# 带搜索框和图表的HTML模板
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>豆瓣读书洞察</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 20px auto; padding: 0 20px; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        img { max-width: 100%; height: auto; }
    </style>
</head>
<body>
    <h1>📚 豆瓣读书 Top250 洞察系统</h1>
    
    <h2>评分分布</h2>
    <img src="data:image/png;base64,{{ plot_url }}" alt="评分分布图">
    
    <h2>搜索书籍</h2>
    <form method="POST">
        <input type="text" name="query" placeholder="输入书名或作者..." value="{{ query }}">
        <button type="submit">搜索</button>
    </form>
    
    {% if query %}
        <h3>搜索结果: {{ books|length }} 条</h3>
    {% else %}
        <h3>展示前20本高分书籍</h3>
    {% endif %}
    
    <table>
        <tr><th>书名</th><th>作者</th><th>评分</th><th>简介</th></tr>
        {% for book in books[:20] %}
        <tr>
            <td>{{ book['title'] }}</td>
            <td>{{ book['author'] }}</td>
            <td>{{ book['rating'] }}</td>
            <td>{{ book['quote'] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    query = ''
    books = []
    if request.method == 'POST':
        query = request.form['query']
        books = search_books(query)
    else:
        books = get_all_books()
    
    plot_url = create_rating_histogram()
    return render_template_string(HTML_TEMPLATE, books=books, query=query, plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)