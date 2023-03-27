import os
import arrow
from flask import Flask, render_template
import frontmatter

app = Flask(__name__,
            static_url_path="",
            static_folder='public')

@app.get('/')
def home():
    context = {
        'page': 'home'
    }
    return render_template('index.html', **context)

@app.get('/contact')
def contact():
    context = {
        'page': 'contact'
    }
    return render_template('contact.html', **context)

@app.get('/posts')
def posts():
    context = {
        'page': 'posts'
    }
    return render_template('posts/index.html', **context)

@app.get('/posts/<path:slug>')
def post(slug: str):
    filename = f'./posts/{slug}.md'
    last_modified = os.path.getmtime(filename)
    post = frontmatter.load(filename)
    post.metadata['last_modified'] = arrow.get(last_modified).to('Asia/Jakarta').format('DD/MM/YYYY HH:mm')
    context = {
        'page': 'posts',
        'meta': post.metadata,
        'content': post.content
    }
    return render_template('posts/view.html', **context)

app.run(port=8080, debug=True)