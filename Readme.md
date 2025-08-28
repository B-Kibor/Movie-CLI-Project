#  Movie Watchlist CLI

A simple **Command Line Interface (CLI)** application to manage a personal TV watchlist.  
Built with **Python** and **SQLAlchemy ORM**, this project demonstrates concepts such as Python fundamentals, OOP, data structures, databases, ORM, and building CLIs.

---

## Features
- User management (create, list, delete users)
- Reviews linked to users
- SQLite database with Alembic migrations
- Clean tabular CLI output with [tabulate]
- Input validation and beginner-friendly design

---

## Requirements
- Python 3.12+
- Virtual environment (recommended)
- Dependencies:
  - SQLAlchemy
  - Alembic
  - Tabulate

---

##  Database Design
The application uses **SQLAlchemy ORM** with 4 related tables:

- **User** → can add reviews  
- **Movie** → belongs to a genre, can have reviews  
- **Review** → links users to movies  
- **Genre** → categorizes movies  

---

## Installation & Setup

1. Clone the repository:
   ```
   git clone <your-repo-url>
   cd Project
   ```
2. Install dependencies:
   ```
   pipenv install
   ```
3. Initialize the database:
   ```
   python cli.py
   ```

## Usage

Run the CLI:
```
python cli.py
```

Menu options:
- 1: Add movie
- 2: List movies
- 3: Delete movie
- 4: List genres
- 5: Add user
- 6: List users
- 7: Delete user
- 8: Add review
- 9: List reviews
- 0: Exit

---

 ## Learning Goals Demonstrated

Python fundamentals → CLI logic, user input/output

Data structures → lists, dicts, tuples in CLI functions

OOP & Inheritance → SQLAlchemy models

SQL & ORM → CRUD operations, relationships

Application structure → modular code
 
## Author

Beatrice Kisabit

## License

MIT License