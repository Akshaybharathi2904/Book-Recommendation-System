from flask import Flask, render_template_string, request
import pandas as pd
import random

app = Flask(__name__)

# Generate random book cover images
def get_book_image(genre):
    colors = {
        'Comedy': ['#FFD700', '#FF6B6B', '#4ECDC4'],
        'Fantasy': ['#9B59B6', '#3498DB', '#E74C3C'],
        'Science Fiction': ['#2C3E50', '#34495E', '#95A5A6'],
        'Mystery': ['#8E44AD', '#2C3E50', '#E67E22'],
        'Romance': ['#E91E63', '#FF69B4', '#FFB6C1'],
        'Horror': ['#8B0000', '#2F4F4F', '#696969'],
        'Classic': ['#8B4513', '#DAA520', '#CD853F']
    }
    color = random.choice(colors.get(genre, ['#667eea']))
    return f"https://via.placeholder.com/200x300/{color[1:]}/ffffff?text={genre.replace(' ', '+')}"

# HTML Template for homepage
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>📚 Ultimate Book Discovery System</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(45deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            margin: 0; padding: 20px; min-height: 100vh;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .container { 
            max-width: 1200px; margin: 0 auto; 
            background: rgba(255, 255, 255, 0.95); padding: 40px; border-radius: 25px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            backdrop-filter: blur(10px);
        }
        
        .header { 
            text-align: center; margin-bottom: 40px; 
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .header h1 { font-size: 3.5em; margin-bottom: 15px; font-weight: bold; }
        .header p { font-size: 1.3em; color: #666; margin-top: 10px; }
        
        .search-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px; border-radius: 20px; margin-bottom: 40px;
            text-align: center; color: white;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        }
        
        .search-title { font-size: 2em; margin-bottom: 25px; font-weight: bold; }
        
        .search-form { 
            display: grid; grid-template-columns: 1fr auto; gap: 20px; 
            max-width: 600px; margin: 0 auto; align-items: center;
        }
        
        .search-input { 
            padding: 18px 25px; border: none; border-radius: 30px; 
            font-size: 18px; box-shadow: 0 8px 25px rgba(0,0,0,0.2);
            transition: all 0.3s;
        }
        
        .search-input:focus {
            outline: none; transform: scale(1.02);
            box-shadow: 0 12px 35px rgba(0,0,0,0.3);
        }
        
        .search-btn { 
            background: linear-gradient(45deg, #ff6b6b, #ff8e53);
            color: white; padding: 18px 35px; border: none; border-radius: 30px; 
            font-size: 18px; font-weight: bold; cursor: pointer; 
            transition: all 0.3s; box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        }
        .search-btn:hover { 
            transform: translateY(-3px); 
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }
        
        .advanced-search {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 30px; border-radius: 20px; margin-bottom: 40px; color: white;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        }
        
        .advanced-title { text-align: center; font-size: 1.5em; margin-bottom: 25px; }
        
        .advanced-form { 
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 20px; align-items: end;
        }
        
        .form-group { display: flex; flex-direction: column; }
        .form-label { margin-bottom: 8px; font-weight: bold; font-size: 14px; }
        .form-input { 
            padding: 12px 18px; border: none; border-radius: 25px; 
            font-size: 14px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .advanced-btn { 
            background: rgba(255,255,255,0.9); color: #333; padding: 12px 25px; 
            border: none; border-radius: 25px; font-weight: bold; cursor: pointer;
            transition: all 0.3s; grid-column: span 2; justify-self: center; min-width: 200px;
        }
        .advanced-btn:hover { background: white; transform: translateY(-2px); }
        
        .stats { 
            display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); 
            gap: 25px; margin: 40px 0;
        }
        .stat-card { 
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white; padding: 30px; border-radius: 20px; text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s;
        }
        .stat-card:hover { transform: translateY(-8px) scale(1.05); }
        .stat-card h3 { font-size: 2.5em; margin-bottom: 10px; }
        .stat-card p { font-size: 1.1em; opacity: 0.9; }
        
        .genres { 
            display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
            gap: 25px; margin-top: 40px;
        }
        .genre-card { 
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 30px; border-radius: 20px; text-align: center; cursor: pointer;
            transition: all 0.4s; box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            position: relative; overflow: hidden;
        }
        
        .genre-card::before {
            content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            transition: left 0.6s;
        }
        .genre-card:hover::before { left: 100%; }
        .genre-card:hover { 
            transform: translateY(-10px) scale(1.05); 
            box-shadow: 0 20px 50px rgba(0,0,0,0.25);
        }
        
        .genre-emoji { font-size: 3em; margin-bottom: 15px; display: block; }
        .genre-title { font-size: 1.4em; font-weight: bold; color: #333; margin-bottom: 10px; }
        .genre-count { color: #666; font-size: 1.1em; font-weight: 500; }
        
        .view-all-btn { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 20px 50px; border: none; border-radius: 35px; 
            font-size: 18px; font-weight: bold; margin: 40px auto; display: block; 
            cursor: pointer; box-shadow: 0 15px 40px rgba(0,0,0,0.2);
            transition: all 0.3s;
        }
        .view-all-btn:hover {
            transform: translateY(-5px); 
            box-shadow: 0 25px 60px rgba(0,0,0,0.3);
        }
        
        .section-title {
            text-align: center; margin: 50px 0 30px; color: #333; font-size: 2.5em;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Ultimate Book Discovery</h1>
            <p>🌟 Explore {{ total_books }} amazing books across {{ genres|length }} exciting genres 🌟</p>
        </div>
        
        <div class="search-section">
            <div class="search-title">🔍 Find Your Next Great Read</div>
            <form class="search-form" action="/search" method="GET">
                <input type="text" name="query" placeholder="Search books, authors, genres..." class="search-input" required>
                <button type="submit" class="search-btn">🚀 Search</button>
            </form>
        </div>
        
        <div class="advanced-search">
            <div class="advanced-title">🎯 Advanced Book Search</div>
            <form class="advanced-form" action="/search" method="GET">
                <div class="form-group">
                    <label class="form-label">📖 Book Title</label>
                    <input type="text" name="title" placeholder="Enter book title..." class="form-input">
                </div>
                <div class="form-group">
                    <label class="form-label">✍️ Author</label>
                    <input type="text" name="author" placeholder="Enter author name..." class="form-input">
                </div>
                <div class="form-group">
                    <label class="form-label">🎭 Genre</label>
                    <select name="genre" class="form-input">
                        <option value="">All Genres</option>
                        {% for genre in genres %}
                        <option value="{{ genre }}">{{ genre }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">📅 Release Year</label>
                    <select name="year" class="form-input">
                        <option value="">Any Year</option>
                        <option value="2020-2024">2020-2024</option>
                        <option value="2010-2019">2010-2019</option>
                        <option value="2000-2009">2000-2009</option>
                        <option value="1990-1999">1990-1999</option>
                        <option value="1950-1989">1950-1989</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">⭐ Min Rating</label>
                    <select name="rating" class="form-input">
                        <option value="">Any Rating</option>
                        <option value="4.5">4.5+ Stars</option>
                        <option value="4.0">4.0+ Stars</option>
                        <option value="3.5">3.5+ Stars</option>
                    </select>
                </div>
                <button type="submit" class="advanced-btn">🎯 Advanced Search</button>
            </form>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <h3>{{ total_books }}</h3>
                <p>📚 Total Books</p>
            </div>
            <div class="stat-card">
                <h3>{{ genres|length }}</h3>
                <p>🎭 Genres</p>
            </div>
            <div class="stat-card">
                <h3>200+</h3>
                <p>📖 Books per Genre</p>
            </div>
            <div class="stat-card">
                <h3>4.0⭐</h3>
                <p>🌟 Avg Rating</p>
            </div>
        </div>
        
        <button class="view-all-btn" onclick="window.location.href='/search?genre=all'">
            📚 Explore All Books
        </button>
        
        <h2 class="section-title">🎭 Browse by Genre</h2>
        <div class="genres">
            {% for genre in genres %}
            <div class="genre-card" onclick="window.location.href='/search?genre={{ genre }}'">
                <span class="genre-emoji">
                    {% if genre == 'Comedy' %}😂
                    {% elif genre == 'Fantasy' %}🧙♂️
                    {% elif genre == 'Science Fiction' %}🚀
                    {% elif genre == 'Mystery' %}🔍
                    {% elif genre == 'Romance' %}💕
                    {% elif genre == 'Horror' %}👻
                    {% elif genre == 'Classic' %}📜
                    {% else %}📚
                    {% endif %}
                </span>
                <div class="genre-title">{{ genre }}</div>
                <div class="genre-count">{{ genre_counts[genre] }} amazing books</div>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

# HTML Template for search results
SEARCH_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>📖 Search Results - Book Discovery</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(45deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            margin: 0; padding: 20px; min-height: 100vh;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .container { 
            max-width: 1400px; margin: 0 auto; 
            background: rgba(255, 255, 255, 0.95); padding: 30px; border-radius: 25px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            backdrop-filter: blur(10px);
        }
        
        .header { 
            display: flex; justify-content: space-between; align-items: center; 
            margin-bottom: 30px; flex-wrap: wrap; gap: 20px;
        }
        .header h1 {
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.5em;
        }
        .back-btn { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 12px 25px; border: none; border-radius: 25px; 
            text-decoration: none; font-weight: bold; transition: transform 0.3s;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .back-btn:hover { transform: translateY(-2px); }
        
        .search-section {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 25px; border-radius: 20px; margin-bottom: 25px; color: white;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .search-title { text-align: center; margin-bottom: 20px; font-size: 1.3em; font-weight: bold; }
        .search-form { 
            display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); 
            gap: 15px; align-items: end;
        }
        .form-group { display: flex; flex-direction: column; }
        .form-label { margin-bottom: 5px; font-size: 14px; font-weight: bold; }
        .search-input { 
            padding: 10px 15px; border: none; border-radius: 20px; 
            font-size: 14px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .search-btn { 
            background: rgba(255,255,255,0.9); color: #333; padding: 12px 20px; 
            border: none; border-radius: 20px; font-weight: bold; cursor: pointer;
            transition: all 0.3s; grid-column: span 2; justify-self: center; min-width: 200px;
        }
        .search-btn:hover { background: white; transform: translateY(-2px); }
        
        .results-info { 
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 20px; border-radius: 15px; margin-bottom: 25px;
            text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .results-info strong { color: #333; font-size: 1.2em; }
        
        .book-grid { 
            display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); 
            gap: 25px; margin-bottom: 30px;
        }
        .book-card { 
            background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
            border: none; padding: 25px; border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            transition: all 0.4s; position: relative; overflow: hidden;
        }
        
        .book-card::before {
            content: ''; position: absolute; top: 0; left: 0; right: 0; height: 5px;
            background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        }
        
        .book-card:hover { 
            transform: translateY(-10px) scale(1.02); 
            box-shadow: 0 20px 50px rgba(0,0,0,0.25);
        }
        
        .book-content { display: flex; gap: 20px; }
        .book-image { 
            width: 80px; height: 120px; border-radius: 10px; 
            background: linear-gradient(135deg, #667eea, #764ba2);
            display: flex; align-items: center; justify-content: center;
            color: white; font-weight: bold; font-size: 12px; text-align: center;
            flex-shrink: 0;
        }
        
        .book-details { flex: 1; }
        .book-title { 
            font-weight: bold; color: #333; margin-bottom: 8px; 
            font-size: 1.3em; line-height: 1.3;
        }
        .book-author { 
            color: #666; margin-bottom: 15px; font-style: italic; font-size: 1.1em;
        }
        
        .book-info { font-size: 14px; color: #555; line-height: 1.6; }
        .book-info > div { margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
        
        .rating { 
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            color: #333; padding: 4px 12px; border-radius: 15px; 
            font-weight: bold; font-size: 13px;
        }
        .price { 
            background: linear-gradient(45deg, #4ecdc4, #44a08d);
            color: white; padding: 4px 12px; border-radius: 15px; 
            font-weight: bold; font-size: 13px;
        }
        .genre-tag {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white; padding: 4px 12px; border-radius: 15px; 
            font-size: 12px; font-weight: bold;
        }
        .year-tag {
            background: linear-gradient(45deg, #ff9a9e, #fecfef);
            color: #333; padding: 4px 12px; border-radius: 15px; 
            font-size: 12px; font-weight: bold;
        }
        
        .pagination { 
            text-align: center; margin: 40px 0;
            display: flex; justify-content: center; flex-wrap: wrap; gap: 10px;
        }
        .pagination a { 
            display: inline-block; padding: 12px 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; text-decoration: none; border-radius: 25px;
            font-weight: bold; transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .pagination a:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.3); }
        .pagination .current { 
            background: linear-gradient(135deg, #ff6b6b 0%, #ffa500 100%);
            transform: scale(1.1);
        }
        
        .no-results { text-align: center; padding: 60px 20px; color: #666; }
        .no-results h2 { font-size: 2em; margin-bottom: 20px; color: #333; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📖 Search Results</h1>
            <a href="/" class="back-btn">← Back to Home</a>
        </div>
        
        <div class="search-section">
            <div class="search-title">🔍 Refine Your Search</div>
            <form class="search-form" action="/search" method="GET">
                <div class="form-group">
                    <label class="form-label">📖 Search Query</label>
                    <input type="text" name="query" placeholder="Books, authors..." class="search-input" value="{{ query }}">
                </div>
                <div class="form-group">
                    <label class="form-label">✍️ Author</label>
                    <input type="text" name="author" placeholder="Author name..." class="search-input" value="{{ author }}">
                </div>
                <div class="form-group">
                    <label class="form-label">🎭 Genre</label>
                    <select name="genre" class="search-input">
                        <option value="">All Genres</option>
                        <option value="Comedy" {% if selected_genre == 'Comedy' %}selected{% endif %}>Comedy</option>
                        <option value="Fantasy" {% if selected_genre == 'Fantasy' %}selected{% endif %}>Fantasy</option>
                        <option value="Science Fiction" {% if selected_genre == 'Science Fiction' %}selected{% endif %}>Science Fiction</option>
                        <option value="Mystery" {% if selected_genre == 'Mystery' %}selected{% endif %}>Mystery</option>
                        <option value="Romance" {% if selected_genre == 'Romance' %}selected{% endif %}>Romance</option>
                        <option value="Horror" {% if selected_genre == 'Horror' %}selected{% endif %}>Horror</option>
                        <option value="Classic" {% if selected_genre == 'Classic' %}selected{% endif %}>Classic</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">📅 Year Range</label>
                    <select name="year" class="search-input">
                        <option value="">Any Year</option>
                        <option value="2020-2024" {% if year_range == '2020-2024' %}selected{% endif %}>2020-2024</option>
                        <option value="2010-2019" {% if year_range == '2010-2019' %}selected{% endif %}>2010-2019</option>
                        <option value="2000-2009" {% if year_range == '2000-2009' %}selected{% endif %}>2000-2009</option>
                        <option value="1990-1999" {% if year_range == '1990-1999' %}selected{% endif %}>1990-1999</option>
                        <option value="1950-1989" {% if year_range == '1950-1989' %}selected{% endif %}>1950-1989</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">⭐ Min Rating</label>
                    <select name="rating" class="search-input">
                        <option value="">Any Rating</option>
                        <option value="4.5" {% if min_rating == '4.5' %}selected{% endif %}>4.5+ Stars</option>
                        <option value="4.0" {% if min_rating == '4.0' %}selected{% endif %}>4.0+ Stars</option>
                        <option value="3.5" {% if min_rating == '3.5' %}selected{% endif %}>3.5+ Stars</option>
                    </select>
                </div>
                <button type="submit" class="search-btn">🔍 Search Books</button>
            </form>
        </div>
        
        <div class="results-info">
            <strong>{{ total_results }}</strong> books found
            {% if query %} for "{{ query }}"{% endif %}
            {% if selected_genre %} in {{ selected_genre }} genre{% endif %}
            {% if author %} by author "{{ author }}"{% endif %}
            {% if year_range %} from {{ year_range }}{% endif %}
            {% if min_rating %} with {{ min_rating }}+ stars{% endif %}
            {% if total_results > 0 %} (Page {{ page }} of {{ total_pages }}){% endif %}
        </div>
        
        {% if books %}
        <div class="book-grid">
            {% for book in books %}
            <div class="book-card">
                <div class="book-content">
                    <div class="book-image">
                        📚<br>{{ book.genre[:3] }}
                    </div>
                    <div class="book-details">
                        <div class="book-title">{{ book.title }}</div>
                        <div class="book-author">by {{ book.author }}</div>
                        <div class="book-info">
                            <div><span class="rating">⭐ {{ book.rating }}/5</span></div>
                            <div><span class="price">${{ book.price }}</span></div>
                            <div><span class="year-tag">📅 {{ book.year }}</span></div>
                            <div>📄 {{ book.pages }} pages</div>
                            <div>🏢 {{ book.publisher }}</div>
                            <div><span class="genre-tag">{{ book.genre }}</span></div>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        
        {% if total_pages > 1 %}
        <div class="pagination">
            {% if page > 1 %}
                <a href="/search?query={{ query }}&author={{ author }}&genre={{ selected_genre }}&year={{ year_range }}&rating={{ min_rating }}&page={{ page - 1 }}">← Previous</a>
            {% endif %}
            
            {% for p in range(1, total_pages + 1) %}
                {% if p == page %}
                    <a href="#" class="current">{{ p }}</a>
                {% elif p <= 3 or p > total_pages - 3 or (p >= page - 2 and p <= page + 2) %}
                    <a href="/search?query={{ query }}&author={{ author }}&genre={{ selected_genre }}&year={{ year_range }}&rating={{ min_rating }}&page={{ p }}">{{ p }}</a>
                {% endif %}
            {% endfor %}
            
            {% if page < total_pages %}
                <a href="/search?query={{ query }}&author={{ author }}&genre={{ selected_genre }}&year={{ year_range }}&rating={{ min_rating }}&page={{ page + 1 }}">Next →</a>
            {% endif %}
        </div>
        {% endif %}
        
        {% else %}
        <div class="no-results">
            <h2>📚 No books found</h2>
            <p>Try different search terms or browse all books.</p>
            <a href="/search?genre=all" class="back-btn" style="display: inline-block; margin-top: 20px;">View All Books</a>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    try:
        books_df = pd.read_csv('data/books.csv')
        genres = books_df['genre'].unique().tolist()
        genre_counts = books_df['genre'].value_counts().to_dict()
        total_books = len(books_df)
        
        return render_template_string(HOME_TEMPLATE, 
                                    genres=genres, 
                                    genre_counts=genre_counts,
                                    total_books=total_books)
    except:
        return "Error: Please run 'python generate_books.py' first to create the database."

@app.route('/search')
def search():
    try:
        books_df = pd.read_csv('data/books.csv')
        
        # Get search parameters
        query = request.args.get('query', '').strip()
        title = request.args.get('title', '').strip()
        author = request.args.get('author', '').strip()
        genre = request.args.get('genre', '').strip()
        year_range = request.args.get('year', '').strip()
        min_rating = request.args.get('rating', '').strip()
        page = int(request.args.get('page', 1))
        per_page = 15
        
        # Filter books
        filtered_books = books_df.copy()
        
        # Genre filter
        if genre and genre != 'all':
            filtered_books = filtered_books[filtered_books['genre'] == genre]
        
        # General query search
        if query:
            mask = (
                filtered_books['title'].str.contains(query, case=False, na=False) |
                filtered_books['author'].str.contains(query, case=False, na=False) |
                filtered_books['genre'].str.contains(query, case=False, na=False)
            )
            filtered_books = filtered_books[mask]
        
        # Title search
        if title:
            filtered_books = filtered_books[filtered_books['title'].str.contains(title, case=False, na=False)]
        
        # Author search
        if author:
            filtered_books = filtered_books[filtered_books['author'].str.contains(author, case=False, na=False)]
        
        # Year range filter
        if year_range:
            if year_range == '2020-2024':
                filtered_books = filtered_books[filtered_books['year'] >= 2020]
            elif year_range == '2010-2019':
                filtered_books = filtered_books[(filtered_books['year'] >= 2010) & (filtered_books['year'] <= 2019)]
            elif year_range == '2000-2009':
                filtered_books = filtered_books[(filtered_books['year'] >= 2000) & (filtered_books['year'] <= 2009)]
            elif year_range == '1990-1999':
                filtered_books = filtered_books[(filtered_books['year'] >= 1990) & (filtered_books['year'] <= 1999)]
            elif year_range == '1950-1989':
                filtered_books = filtered_books[(filtered_books['year'] >= 1950) & (filtered_books['year'] <= 1989)]
        
        # Rating filter
        if min_rating:
            try:
                min_rating_float = float(min_rating)
                filtered_books = filtered_books[filtered_books['rating'] >= min_rating_float]
            except ValueError:
                pass
        
        # Sort by rating
        filtered_books = filtered_books.sort_values('rating', ascending=False)
        
        # Pagination
        total_results = len(filtered_books)
        total_pages = (total_results + per_page - 1) // per_page
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        page_books = filtered_books.iloc[start_idx:end_idx]
        
        return render_template_string(SEARCH_TEMPLATE,
                                    books=page_books.to_dict('records'),
                                    query=query,
                                    author=author,
                                    selected_genre=genre,
                                    year_range=year_range,
                                    min_rating=min_rating,
                                    page=page,
                                    total_pages=total_pages,
                                    total_results=total_results)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    print("Starting Enhanced Book Discovery System...")
    print("Open your browser and go to: http://localhost:5000")
    print("Database: 1400 books with enhanced search features")
    print("Features: Book images, release dates, colorful UI")
    print("Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='localhost', port=5000)