from database import SessionLocal, init_db
from models import Movie, Genre

#  MOVIE COMMANDS
def add_movie():
    session = SessionLocal()
    try:
        title = input("Enter movie title: ")
        genre_name = input("Enter genre: ")

        # Check if genre exists, otherwise create
        genre = session.query(Genre).filter_by(name=genre_name).first()
        if not genre:
            genre = Genre(name=genre_name)
            session.add(genre)
            session.commit()
            session.refresh(genre)

        # Add movie
        movie = Movie(title=title, genre=genre)
        session.add(movie)
        session.commit()
        print(f"Movie '{title}' added under genre '{genre_name}'")
    finally:
        session.close()


def list_movies():
    session = SessionLocal()
    try:
        movies = session.query(Movie).all()
        if not movies:
            print("No movies found.")
            return
        print("\nMovies:")
        for movie in movies:
            print(f"{movie.id}. {movie.title} ({movie.genre.name if movie.genre else 'No genre'})")
    finally:
        session.close()


def delete_movie():
    session = SessionLocal()
    try:
        list_movies()
        movie_id = input("\nEnter movie ID to delete (or press Enter to cancel): ").strip()
        if not movie_id:
            print("Cancelled.")
            return

        movie = session.query(Movie).get(int(movie_id))
        if not movie:
            print(f"No movie found with ID {movie_id}")
            return

        session.delete(movie)
        session.commit()
        print(f" Movie '{movie.title}' deleted successfully")
    finally:
        session.close()


def list_genres():
    session = SessionLocal()
    try:
        genres = session.query(Genre).all()
        if not genres:
            print(" No genres found.")
            return
        print("\n Genres:")
        for genre in genres:
            print(f"- {genre.name}")
    finally:
        session.close()

#  MENU LOOP
def main():
    init_db()

    while True:
        print("\n Movie/TV Watchlist CLI")
        print("1. Add movie")
        print("2. List movies")
        print("3. Delete movie")
        print("4. List genres")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_movie()
        elif choice == "2":
            list_movies()
        elif choice == "3":
            delete_movie()
        elif choice == "4":
            list_genres()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
