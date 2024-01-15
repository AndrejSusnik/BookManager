import psycopg2
from config_managment import CustomConfigManager
import sys
import bcrypt

def seed_users(cur):
    print("Seeding users: ", end='')
    try:
        for i in range(20):
            cur.execute(f"INSERT INTO users (name, password, email) VALUES ('user{i}', '{bcrypt.hashpw(('password' + str(i)).encode('utf-8'), bcrypt.gensalt( 12 )).decode()}', '{i}@gmail.com');")
            print('.', end='')
        print(' successful')
    except psycopg2.errors.UniqueViolation:
        print(' failed')
        print('Reson for failure: UniqueViolation')

def seed_read_books(cur):
    print("Seeding read_books: ", end='')
    try:
        for i in range(1, 21):
            print('.', end='')
            for j in range(10):
                cur.execute(f"INSERT INTO read_books (user_id, title, review, rating) VALUES ({i}, 'book{j}', 'review', {j});")
        print(' successful')
    except psycopg2.errors.ForeignKeyViolation:
        print(' failed')
        print('Reson for failure: ForeignKeyViolation')


def create_tables(cur):
    print("Creating tables: ", end='')
    try:
        cur.execute("CREATE TABLE users (id serial PRIMARY KEY, name varchar NOT NULL UNIQUE, password varchar NOT NULL, email varchar);")
        cur.execute("CREATE TABLE read_books (id serial PRIMARY KEY, user_id integer NOT NULL, title varchar NOT NULL, review varchar NOT NULL, rating integer NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id));")
        print(' successful')
    except psycopg2.errors.DuplicateTable:
        print(' failed')
        print('Reson for failure: DuplicateTable')

def drop_tables(cur):
    print("Dropping tables: ", end='')
    try:
        cur.execute("DROP TABLE IF EXISTS read_books;")
        cur.execute("DROP TABLE IF EXISTS users;")
        print(' successful')
    except Exception as e:
        print(' failed')
        print(f'Reson for failure: {e}')

if __name__ == '__main__':
    config = CustomConfigManager("./")
    host = config.get("DB_URL", default="localhost")
    db_name = config.get("DB_NAME", default="postgres")
    username = config.get("DB_USER", default="postgres")
    password = config.get("DB_PASSWORD", default="postgres")

    db = psycopg2.connect(host=host, database=db_name, user=username, password=password)
    cursor = db.cursor()

    try:
        if len(sys.argv) == 1:
            print("Usage: python db_cli.py [create|drop|seed|reset]")
            exit(1)

        elif sys.argv[1] == "create":
            create_tables(cursor)
            print("Tables created successfully")
        elif sys.argv[1] == "drop":
            drop_tables(cursor)
            print("Tables dropped successfully")
        elif sys.argv[1] == "seed":
            seed_users(cursor)
            seed_read_books(cursor)
            print("Tables seeded successfully")
        elif sys.argv[1] == "reset":
            drop_tables(cursor)
            create_tables(cursor)
            seed_users(cursor)
            seed_read_books(cursor)
            print("Tables reset successfully")
    except Exception as e:
        print("Error: ", e)
        db.rollback()
    finally:
        db.commit()
        cursor.close()
        db.close()
    