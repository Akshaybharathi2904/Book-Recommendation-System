from src.recommendation_system import BookRecommendationSystem
import pandas as pd
import numpy as np

def create_sample_data():
    """Create expanded book data with genres"""
    books = [
        # Comedy Books
        {'title': 'Good Omens', 'author': 'Terry Pratchett', 'genre': 'Comedy', 'rating': 4.3, 'description': 'A hilarious collaboration about the apocalypse'},
        {'title': 'The Hitchhiker\'s Guide to the Galaxy', 'author': 'Douglas Adams', 'genre': 'Comedy', 'rating': 4.2, 'description': 'The funniest science fiction comedy ever written'},
        {'title': 'Bridget Jones\'s Diary', 'author': 'Helen Fielding', 'genre': 'Comedy', 'rating': 3.9, 'description': 'A hilarious diary of a single woman in London'},
        {'title': 'Me Talk Pretty One Day', 'author': 'David Sedaris', 'genre': 'Comedy', 'rating': 4.1, 'description': 'Witty and self-deprecating essays about life'},
        {'title': 'Bossypants', 'author': 'Tina Fey', 'genre': 'Comedy', 'rating': 4.0, 'description': 'Hilarious memoir about comedy and motherhood'},
        {'title': 'Yes Please', 'author': 'Amy Poehler', 'genre': 'Comedy', 'rating': 3.8, 'description': 'Funny memoir about life and career'},
        {'title': 'Catch-22', 'author': 'Joseph Heller', 'genre': 'Comedy', 'rating': 4.2, 'description': 'A darkly comic novel about the absurdity of war'},
        {'title': 'The Rosie Project', 'author': 'Graeme Simsion', 'genre': 'Comedy', 'rating': 4.0, 'description': 'A romantic comedy about a genetics professor seeking love'},
        {'title': 'Where\'d You Go, Bernadette', 'author': 'Maria Semple', 'genre': 'Comedy', 'rating': 3.9, 'description': 'A witty novel about a missing mother and family dysfunction'},
        {'title': 'A Confederacy of Dunces', 'author': 'John Kennedy Toole', 'genre': 'Comedy', 'rating': 4.1, 'description': 'A comic masterpiece about an eccentric man in New Orleans'},
        
        # Fantasy Books
        {'title': 'The Lord of the Rings', 'author': 'J.R.R. Tolkien', 'genre': 'Fantasy', 'rating': 4.5, 'description': 'An epic fantasy adventure in Middle-earth'},
        {'title': 'Harry Potter', 'author': 'J.K. Rowling', 'genre': 'Fantasy', 'rating': 4.4, 'description': 'A magical story about a young wizard'},
        {'title': 'Game of Thrones', 'author': 'George R.R. Martin', 'genre': 'Fantasy', 'rating': 4.3, 'description': 'Epic fantasy about power, politics, and dragons'},
        {'title': 'The Name of the Wind', 'author': 'Patrick Rothfuss', 'genre': 'Fantasy', 'rating': 4.2, 'description': 'A beautifully written fantasy about music and magic'},
        {'title': 'Mistborn', 'author': 'Brandon Sanderson', 'genre': 'Fantasy', 'rating': 4.4, 'description': 'Epic fantasy with unique magic system'},
        
        # Science Fiction Books
        {'title': 'Dune', 'author': 'Frank Herbert', 'genre': 'Science Fiction', 'rating': 4.2, 'description': 'A science fiction epic about desert planet Arrakis'},
        {'title': 'Foundation', 'author': 'Isaac Asimov', 'genre': 'Science Fiction', 'rating': 4.1, 'description': 'A science fiction series about galactic empire'},
        {'title': 'The Martian', 'author': 'Andy Weir', 'genre': 'Science Fiction', 'rating': 4.3, 'description': 'A survival story about an astronaut stranded on Mars'},
        {'title': 'Neuromancer', 'author': 'William Gibson', 'genre': 'Science Fiction', 'rating': 3.9, 'description': 'A cyberpunk novel about virtual reality'},
        {'title': 'Ender\'s Game', 'author': 'Orson Scott Card', 'genre': 'Science Fiction', 'rating': 4.0, 'description': 'A military science fiction novel about child soldiers'},
        
        # Mystery Books
        {'title': 'Gone Girl', 'author': 'Gillian Flynn', 'genre': 'Mystery', 'rating': 4.1, 'description': 'A psychological thriller about a marriage gone wrong'},
        {'title': 'The Girl with the Dragon Tattoo', 'author': 'Stieg Larsson', 'genre': 'Mystery', 'rating': 4.2, 'description': 'A gripping thriller about investigating murders'},
        {'title': 'Sherlock Holmes', 'author': 'Arthur Conan Doyle', 'genre': 'Mystery', 'rating': 4.3, 'description': 'Classic detective stories featuring brilliant detective'},
        {'title': 'The Da Vinci Code', 'author': 'Dan Brown', 'genre': 'Mystery', 'rating': 3.8, 'description': 'A mystery involving religious symbols and secrets'},
        {'title': 'Big Little Lies', 'author': 'Liane Moriarty', 'genre': 'Mystery', 'rating': 4.0, 'description': 'A mystery about three women and their dark secrets'},
        
        # Romance Books
        {'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'genre': 'Romance', 'rating': 4.0, 'description': 'A romantic novel about manners and marriage'},
        {'title': 'The Notebook', 'author': 'Nicholas Sparks', 'genre': 'Romance', 'rating': 4.1, 'description': 'A tearjerker romance about enduring love'},
        {'title': 'Me Before You', 'author': 'Jojo Moyes', 'genre': 'Romance', 'rating': 4.2, 'description': 'A heartbreaking romance about love and loss'},
        {'title': 'Outlander', 'author': 'Diana Gabaldon', 'genre': 'Romance', 'rating': 4.3, 'description': 'A time-traveling historical romance'},
        {'title': 'The Hating Game', 'author': 'Sally Thorne', 'genre': 'Romance', 'rating': 4.0, 'description': 'A workplace enemies-to-lovers romance'},
        
        # Horror Books
        {'title': 'The Shining', 'author': 'Stephen King', 'genre': 'Horror', 'rating': 4.2, 'description': 'A terrifying horror novel about a haunted hotel'},
        {'title': 'Dracula', 'author': 'Bram Stoker', 'genre': 'Horror', 'rating': 4.0, 'description': 'The classic vampire novel that started it all'},
        {'title': 'Frankenstein', 'author': 'Mary Shelley', 'genre': 'Horror', 'rating': 3.9, 'description': 'The original monster story about science and creation'},
        {'title': 'It', 'author': 'Stephen King', 'genre': 'Horror', 'rating': 4.1, 'description': 'A horror novel about a shape-shifting entity'},
        {'title': 'The Exorcist', 'author': 'William Peter Blatty', 'genre': 'Horror', 'rating': 4.0, 'description': 'A chilling horror novel about demonic possession'},
        
        # Classic Literature
        {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'genre': 'Classic', 'rating': 4.3, 'description': 'A story of racial injustice and childhood innocence'},
        {'title': '1984', 'author': 'George Orwell', 'genre': 'Classic', 'rating': 4.1, 'description': 'A dystopian novel about totalitarian control'},
        {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'genre': 'Classic', 'rating': 4.2, 'description': 'A classic American novel about the Jazz Age'},
        {'title': 'The Catcher in the Rye', 'author': 'J.D. Salinger', 'genre': 'Classic', 'rating': 3.8, 'description': 'A coming-of-age story in New York'},
        {'title': 'Lord of the Flies', 'author': 'William Golding', 'genre': 'Classic', 'rating': 3.9, 'description': 'A novel about civilization and savagery'}
    ]
    
    # Convert to DataFrame
    books_df = pd.DataFrame(books)
    books_df['book_id'] = range(1, len(books) + 1)
    return books_df[['book_id', 'title', 'author', 'genre', 'rating', 'description']]

def search_books_by_genre(books_df, genre):
    """Search books by genre"""
    genre_books = books_df[books_df['genre'].str.contains(genre, case=False, na=False)]
    return genre_books[['title', 'author', 'genre', 'rating']].sort_values('rating', ascending=False)

def main():
    # Create recommendation system
    recommender = BookRecommendationSystem()
    
    # Create and save sample data
    books_df = create_sample_data()
    books_df.to_csv('data/books.csv', index=False)
    
    # Load data
    recommender.load_data('data/books.csv')
    
    print("Book Recommendation System")
    print("=" * 50)
    
    # Show available genres
    print("\nAvailable Genres:")
    genres = books_df['genre'].unique()
    for i, genre in enumerate(genres, 1):
        count = len(books_df[books_df['genre'] == genre])
        print(f"{i}. {genre} ({count} books)")
    
    # Search for comedy books
    print("\n" + "=" * 50)
    print("COMEDY BOOKS:")
    print("=" * 50)
    comedy_books = search_books_by_genre(books_df, 'Comedy')
    print(comedy_books.to_string(index=False))
    
    # Show other genre examples
    print("\n" + "=" * 50)
    print("FANTASY BOOKS:")
    print("=" * 50)
    fantasy_books = search_books_by_genre(books_df, 'Fantasy')
    print(fantasy_books.to_string(index=False))
    
    print("\n" + "=" * 50)
    print("SCIENCE FICTION BOOKS:")
    print("=" * 50)
    scifi_books = search_books_by_genre(books_df, 'Science Fiction')
    print(scifi_books.to_string(index=False))
    
    print(f"\nTotal books in database: {len(books_df)}")
    print("You can now search for any genre!")

if __name__ == "__main__":
    main()