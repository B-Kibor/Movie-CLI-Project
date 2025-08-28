# cli.py
from tabulate import tabulate
from database import SessionLocal, init_db
from models import User, Movie, Review, Genre


def get_session():
    """Open a database session safely."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        raise
    finally:
        session.close()

def prompt_nonempty(message):
    """Ask until a non-empty string is entered."""
    while True:
        value = input(message).strip()
        if value:
            return value
        print("Input cannot be empty. Try again.")

def prompt_int(message, lo=None, hi=None):
    """Ask until a valid integer is entered (with optional limits)."""
    while True:
        try:
            number = int(input(message).strip())
            if lo is not None and number < lo:
                print(f"Value must be ≥ {lo}")
                continue
            if hi is not None and number > hi:
                print(f"Value must be ≤ {hi}")
                continue
            return number
        except ValueError:
            print("Enter a valid integer.")

def choose_from_list(items, label=str, allow_skip=False):
    """Show a list and let the user choose an item."""
    if not items:
        print("Nothing to choose from.")
        return None

    table = [(i + 1, label(x)) for i, x in enumerate(items)]
    print(tabulate(table, headers=["#", "Choice"], tablefmt="github"))

    if allow_skip:
        print("0. Skip")

    choice = prompt_int("Select: ", 0 if allow_skip else 1, len(items))
    if choice == 0 and allow_skip:
        return None
    return items[choice - 1]

# ---------------- Movie Commands ---------------- #

def add_movie():
    title = prompt_nonempty("Movie title: ")
    genre_name = prompt_nonempty("Genre: ")

    for session in get_session():
        genre = session.query(Genre).filter_by(name=genre_name).first()
        if not genre:
            genre = Genre(name=genre_name)
            session.add(genre)
            session.flush()

        if session.query(Movie).filter_by(title=title, genre_id=genre.id).first():
            print("This movie already exists.")
            return

        movie = Movie(title=title, genre=genre)
        session.add(movie)
        print(f"'{title}' added under genre '{genre_name}'.")

def list_movies():
    for session in get_session():
        movies = (
            session.query(Movie)
            .outerjoin(Genre)
            .with_entities(Movie.id, Movie.title, Genre.name)
            .all()
        )
        if not movies:
            print("No movies found.")
        else:
            print(tabulate(movies, headers=["ID", "Title", "Genre"], tablefmt="github"))

def delete_movie():
    for session in get_session():
        movies = session.query(Movie).all()
        if not movies:
            print("No movies found.")
            return

        print(tabulate([(m.id, m.title) for m in movies], headers=["ID", "Title"], tablefmt="github"))
        movie_id = prompt_int("Enter movie ID to delete: ")
        movie = session.get(Movie, movie_id)

        if not movie:
            print("Movie not found.")
            return

        session.delete(movie)
        print(f"'{movie.title}' deleted.")

def list_genres():
    for session in get_session():
        genres = session.query(Genre).all()
        if not genres:
            print("No genres found.")
        else:
            print(tabulate([(g.id, g.name) for g in genres], headers=["ID", "Genre"], tablefmt="github"))

# ---------------- User Commands ---------------- #

def add_user():
    username = prompt_nonempty("Username: ")
    email = input("Email (optional): ").strip() or None

    for session in get_session():
        if session.query(User).filter_by(username=username).first():
            print("Username already exists.")
            return
        if email and session.query(User).filter_by(email=email).first():
            print("Email already exists.")
            return

        user = User(username=username, email=email)
        session.add(user)
        print(f"User '{username}' added.")

def list_users():
    for session in get_session():
        users = session.query(User).all()
        if not users:
            print("No users found.")
        else:
            table = [(u.id, u.username, u.email or "-") for u in users]
            print(tabulate(table, headers=["ID", "Username", "Email"], tablefmt="github"))

def delete_user():
    for session in get_session():
        users = session.query(User).all()
        if not users:
            print("No users found.")
            return

        print(tabulate([(u.id, u.username) for u in users], headers=["ID", "Username"], tablefmt="github"))
        user_id = prompt_int("Enter user ID to delete: ")
        user = session.get(User, user_id)

        if not user:
            print("User not found.")
            return

        session.delete(user)
        print(f"'{user.username}' deleted.")

# ---------------- Review Commands ---------------- #

def add_review():
    for session in get_session():
        user = choose_from_list(session.query(User).all(), lambda u: f"{u.username} (id={u.id})")
        movie = choose_from_list(session.query(Movie).all(), lambda m: f"{m.title} (id={m.id})")

        if not user or not movie:
            return

        if session.query(Review).filter_by(user_id=user.id, movie_id=movie.id).first():
            print("Already reviewed this movie.")
            return

        rating = prompt_int("Rating (1-5): ", 1, 5)
        comment = input("Comment: ").strip() or None

        review = Review(user=user, movie=movie, rating=rating, comment=comment)
        session.add(review)
        print(f"{user.username} rated '{movie.title}' {rating}/5.")

def list_reviews():
    for session in get_session():
        reviews = (
            session.query(Review)
            .join(User)
            .join(Movie)
            .with_entities(Review.id, User.username, Movie.title, Review.rating, Review.comment, Review.created_at)
            .all()
        )
        if not reviews:
            print("No reviews found.")
        else:
            print(tabulate(reviews, headers=["ID", "User", "Movie", "Rating", "Comment", "Created"], tablefmt="github"))

# ---------------- CLI Menu ---------------- #

def main_menu():
    print("\n--- Movie Watchlist CLI ---")
    print("1. Add movie")
    print("2. List movies")
    print("3. Delete movie")
    print("4. List genres")
    print("5. Add user")
    print("6. List users")
    print("7. Delete user")
    print("8. Add review")
    print("9. List reviews")
    print("0. Exit")

COMMANDS = {
    "1": add_movie,
    "2": list_movies,
    "3": delete_movie,
    "4": list_genres,
    "5": add_user,
    "6": list_users,
    "7": delete_user,
    "8": add_review,
    "9": list_reviews,
}

def main():
    init_db()
    while True:
        main_menu()
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("See you on the next one buddy!")
            break
        action = COMMANDS.get(choice)
        if action:
            action()
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
