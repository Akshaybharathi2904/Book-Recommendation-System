import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD

class BookRecommendationSystem:
    def __init__(self):
        self.books_df = None
        self.ratings_df = None
        self.tfidf_matrix = None
        self.cosine_sim = None
        
    def load_data(self, books_path, ratings_path=None):
        """Load books and ratings data"""
        self.books_df = pd.read_csv(books_path)
        if ratings_path:
            self.ratings_df = pd.read_csv(ratings_path)
    
    def content_based_recommendation(self, book_title, num_recommendations=5):
        """Content-based filtering using book descriptions"""
        if self.tfidf_matrix is None:
            tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
            self.tfidf_matrix = tfidf.fit_transform(self.books_df['description'].fillna(''))
            self.cosine_sim = cosine_similarity(self.tfidf_matrix)
        
        # Find book index
        idx = self.books_df[self.books_df['title'] == book_title].index[0]
        
        # Get similarity scores
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top recommendations
        book_indices = [i[0] for i in sim_scores[1:num_recommendations+1]]
        return self.books_df.iloc[book_indices][['title', 'author', 'rating']]
    
    def collaborative_filtering(self, user_id, num_recommendations=5):
        """Collaborative filtering using user ratings"""
        if self.ratings_df is None:
            return "Ratings data not available"
        
        # Create user-item matrix
        user_item_matrix = self.ratings_df.pivot_table(
            index='user_id', columns='book_id', values='rating'
        ).fillna(0)
        
        # Apply SVD
        svd = TruncatedSVD(n_components=50)
        matrix_svd = svd.fit_transform(user_item_matrix)
        
        # Calculate user similarities
        user_similarity = cosine_similarity(matrix_svd)
        user_idx = list(user_item_matrix.index).index(user_id)
        
        # Get similar users
        sim_scores = list(enumerate(user_similarity[user_idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Recommend books from similar users
        similar_users = [i[0] for i in sim_scores[1:6]]
        recommendations = []
        
        for similar_user in similar_users:
            user_books = user_item_matrix.iloc[similar_user]
            top_books = user_books.nlargest(num_recommendations)
            recommendations.extend(top_books.index.tolist())
        
        return list(set(recommendations))[:num_recommendations]
    
    def search_by_genre(self, genre, num_results=None):
        """Search books by genre"""
        if self.books_df is None:
            return "Books data not loaded"
        
        genre_books = self.books_df[self.books_df['genre'].str.contains(genre, case=False, na=False)]
        result = genre_books[['title', 'author', 'genre', 'rating']].sort_values('rating', ascending=False)
        
        if num_results:
            return result.head(num_results)
        return result
    
    def get_all_genres(self):
        """Get all available genres"""
        if self.books_df is None:
            return []
        return self.books_df['genre'].unique().tolist()