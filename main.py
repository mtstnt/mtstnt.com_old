from dataclasses import dataclass
from datetime import datetime
from math import ceil
import os
from re import search
import arrow
from flask import Flask, render_template, request
import frontmatter
from pathlib import Path

POST_COUNT_PER_PAGE = 10

app = Flask(__name__,
            static_url_path="",
            static_folder='public')

def get_value_or(val, alternative) -> any:
    return val if val else alternative

@dataclass
class Post:
    slug: str
    title: str
    description: str = ""
    excerpt: str = ""
    keywords: str = ""
    is_draft: bool = False
    published_at: datetime = datetime.now()

    @staticmethod
    def from_frontmatter(post: frontmatter.Post, filename: str) -> 'Post':
        return Post(
            slug=filename,
            title=post.get('title', ''),
            description=post.get('description', ''),
            excerpt=post.get('excerpt', ''),
            keywords=post.get('keywords', ''),
            is_draft=post.get('is_draft', False),
            published_at=post.get('published_at', None),
        )
    
# 1 - 10
# 11 - 20 
# 21 - 30
# 31 - 40
def get_posts(path: str, offset: int = 0, count: int = 10, search_query: str = '') -> Post:
    posts, entries = [], sorted(Path(path).iterdir(), key=os.path.getmtime)
    for entry in entries:
        posts.append(Post.from_frontmatter(frontmatter.load(str(entry)), entry.name.removesuffix('.md')))
    if search_query != '':
        search_query = search_query.lower()
        posts = filter(
                lambda p: (
                    p.title.lower().find(search_query) != -1 or
                    p.slug.lower().find(search_query) != -1 
                ), posts)

    return list(posts)[(offset - 1):(offset - 1)+count]

@app.get('/')
def home():
    page = request.args.get('p', 1)
    query = request.args.get('q', '')
    posts = get_posts('./posts', (int(page) - 1) * POST_COUNT_PER_PAGE + 1, POST_COUNT_PER_PAGE, query)
    context = {
        'page': 'blog',
        'posts': posts,
        'query': query,
        'prev_link': (f'/?p={int(page) - 1}' 
                      if int(page) > 1 
                      else None),
        'next_link': (f'/?p={int(page) + 1}' 
                      if int(page) != ceil(len(os.listdir('./posts')) / POST_COUNT_PER_PAGE) 
                      else None),
    }
    return render_template('index.html', **context)

@app.get('/resume')
def contact():
    context = {
        'page': 'resume'
    }
    return render_template('resume.html', **context)

# @app.get('/blog')
# def blog_home():
#     page = request.args.get('p', 1)
#     query = request.args.get('q', '')
#     posts = get_posts('./posts', (int(page) - 1) * POST_COUNT_PER_PAGE + 1, POST_COUNT_PER_PAGE, query)
#     context = {
#         'page': 'blog',
#         'posts': posts,
#     }
#     return render_template('posts/index.html', **context)

@app.get('/blog/<path:slug>')
def post(slug: str):
    filename = f'./posts/{slug}.md'
    post = frontmatter.load(filename)
    context = {
        'page': 'blog',
        'meta': post.metadata,
        'content': post.content
    }
    return render_template('posts/view.html', **context)

app.run(port=8080, debug=True)