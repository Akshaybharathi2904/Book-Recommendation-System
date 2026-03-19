import pandas as pd
import numpy as np
import random

def generate_massive_book_database():
    """Generate 200+ books per genre with ratings and prices"""
    
    # Base book templates for each genre
    comedy_books = [
        "Good Omens", "Hitchhiker's Guide", "Catch-22", "Bridget Jones", "Bossypants",
        "Yes Please", "Me Talk Pretty", "Rosie Project", "Confederacy of Dunces", "Three Men in a Boat",
        "Importance of Being Earnest", "Diary of a Wimpy Kid", "Captain Underpants", "Dork Diaries",
        "Big Nate", "Smile", "New Kid", "Dog Man", "Amulet", "Bone"
    ]
    
    fantasy_books = [
        "Lord of the Rings", "Harry Potter", "Game of Thrones", "Name of the Wind", "Mistborn",
        "Wheel of Time", "Chronicles of Narnia", "Earthsea", "Dark Tower", "American Gods",
        "Stormlight Archive", "First Law", "Kingkiller Chronicle", "Malazan", "Discworld",
        "Dresden Files", "Inheritance Cycle", "Percy Jackson", "His Dark Materials", "Redwall"
    ]
    
    scifi_books = [
        "Dune", "Foundation", "Martian", "Neuromancer", "Ender's Game",
        "Hitchhiker's Guide", "Blade Runner", "Time Machine", "War of Worlds", "Fahrenheit 451",
        "Handmaid's Tale", "Left Hand of Darkness", "Hyperion", "Snow Crash", "Ready Player One",
        "Expanse", "Old Man's War", "Starship Troopers", "I Robot", "Stranger in Strange Land"
    ]
    
    mystery_books = [
        "Gone Girl", "Girl with Dragon Tattoo", "Sherlock Holmes", "Da Vinci Code", "Big Little Lies",
        "Murder on Orient Express", "And Then There Were None", "Maltese Falcon", "Big Sleep",
        "Girl on the Train", "Silent Patient", "Seven Husbands", "Thursday Murder Club", "Tana French",
        "Louise Penny", "Agatha Christie", "Raymond Chandler", "Dashiell Hammett", "John le Carre", "Michael Crichton"
    ]
    
    romance_books = [
        "Pride and Prejudice", "Notebook", "Me Before You", "Outlander", "Hating Game",
        "Beach Read", "People We Meet", "Seven Husbands", "Time Traveler's Wife", "Fault in Our Stars",
        "Eleanor Oliphant", "Red White Royal Blue", "Kiss Quotient", "Unhoneymooners", "Wedding Date",
        "Proposal", "Royal We", "Beach House", "Summer Sisters", "Elin Hilderbrand"
    ]
    
    horror_books = [
        "Shining", "Dracula", "Frankenstein", "It", "Exorcist",
        "Pet Sematary", "Carrie", "Salem's Lot", "Haunting Hill House", "Turn of the Screw",
        "World War Z", "Bird Box", "Silence of Lambs", "Psycho", "Rosemary's Baby",
        "Interview Vampire", "Something Wicked", "Hell House", "Ghost Story", "Books of Blood"
    ]
    
    classic_books = [
        "To Kill Mockingbird", "1984", "Great Gatsby", "Catcher in Rye", "Lord of Flies",
        "Animal Farm", "Brave New World", "Jane Eyre", "Wuthering Heights", "Moby Dick",
        "War and Peace", "Crime and Punishment", "Brothers Karamazov", "Anna Karenina", "Ulysses",
        "Odyssey", "Iliad", "Divine Comedy", "Canterbury Tales", "Don Quixote"
    ]
    
    authors = [
        "Stephen King", "J.K. Rowling", "George R.R. Martin", "Agatha Christie", "Isaac Asimov",
        "Terry Pratchett", "Neil Gaiman", "Brandon Sanderson", "Patrick Rothfuss", "Douglas Adams",
        "Gillian Flynn", "Tana French", "Louise Penny", "John Green", "Nicholas Sparks",
        "Jane Austen", "Charlotte Bronte", "Emily Bronte", "Charles Dickens", "Mark Twain",
        "Ernest Hemingway", "F. Scott Fitzgerald", "George Orwell", "Aldous Huxley", "Ray Bradbury"
    ]
    
    publishers = [
        "Penguin Random House", "HarperCollins", "Macmillan", "Simon & Schuster", "Hachette",
        "Scholastic", "Pearson", "Wiley", "Oxford University Press", "Cambridge University Press"
    ]
    
    all_books = []
    book_id = 1
    
    genres = {
        'Comedy': comedy_books,
        'Fantasy': fantasy_books,
        'Science Fiction': scifi_books,
        'Mystery': mystery_books,
        'Romance': romance_books,
        'Horror': horror_books,
        'Classic': classic_books
    }
    
    for genre, base_books in genres.items():
        for i in range(200):  # Generate 200 books per genre
            base_title = random.choice(base_books)
            
            # Create variations of titles
            variations = [
                f"{base_title}",
                f"{base_title}: The Beginning",
                f"{base_title}: Part {random.randint(1, 10)}",
                f"The {base_title}",
                f"{base_title} Chronicles",
                f"{base_title} Series",
                f"Return to {base_title}",
                f"{base_title}: A New Chapter",
                f"Beyond {base_title}",
                f"{base_title} Revisited"
            ]
            
            title = random.choice(variations)
            if i > 0:  # Add numbers to make unique
                title = f"{title} #{i+1}"
            
            book = {
                'book_id': book_id,
                'title': title,
                'author': random.choice(authors),
                'genre': genre,
                'rating': round(random.uniform(3.0, 5.0), 1),
                'price': round(random.uniform(9.99, 29.99), 2),
                'pages': random.randint(150, 800),
                'publisher': random.choice(publishers),
                'year': random.randint(1950, 2024),
                'isbn': f"978-{random.randint(1000000000, 9999999999)}",
                'description': f"An amazing {genre.lower()} book that will captivate readers with its engaging story and memorable characters."
            }
            
            all_books.append(book)
            book_id += 1
    
    return pd.DataFrame(all_books)

if __name__ == "__main__":
    print("Generating massive book database...")
    books_df = generate_massive_book_database()
    books_df.to_csv('data/books.csv', index=False)
    print(f"Generated {len(books_df)} books across {books_df['genre'].nunique()} genres")
    print(f"Books per genre: {books_df.groupby('genre').size().to_dict()}")