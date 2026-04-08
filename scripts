import pandas as pd

def show_comedy_books():
    """Demo script to show comedy books"""
    # Load the book data
    books_df = pd.read_csv('data/books.csv')
    
    print("COMEDY BOOK COLLECTION")
    print("=" * 60)
    
    # Filter comedy books
    comedy_books = books_df[books_df['genre'] == 'Comedy'].sort_values('rating', ascending=False)
    
    print(f"Found {len(comedy_books)} comedy books:\n")
    
    for idx, book in comedy_books.iterrows():
        print(f"{book['title']}")
        print(f"  Author: {book['author']}")
        print(f"  Rating: {book['rating']}/5.0")
        print(f"  Description: {book['description']}")
        print("-" * 50)
    
    avg_rating = comedy_books['rating'].mean()
    print(f"\nAverage rating for comedy books: {avg_rating:.1f}/5.0")
    print(f"Highest rated: {comedy_books.iloc[0]['title']} ({comedy_books.iloc[0]['rating']}/5.0)")

if __name__ == "__main__":
    show_comedy_books()