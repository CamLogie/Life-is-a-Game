import click
import psycopg2
import os

from werkzeug.security import generate_password_hash

from flask import current_app, g

def get_db():
    """Get connection to the database"""
    conn = psycopg2.connect(
        host="localhost",
        database="life_is_a_game_db",
        user=os.environ["DATABASE_USER"],
        password=os.environ["DATABASE_PASSWORD"]
    )
    return conn

def close_db(conn, cur):
    """Close the database connection and cursor"""
    cur.close()
    conn.close()

def results_to_dict(cur):
    """Return the results of the previous SQL query in a dict with column name as key"""
    dict = {}
    results = cur.fetchone()

    i = 0
    for x in cur.description:
        dict[x[0]] = results[i]
        i += 1

    return dict

def init_db():
    """Initializes the database by making three tables, users, transactions, and wallet"""
    conn = get_db()
    cur = conn.cursor()

    cur.execute('''DROP TABLE IF EXISTS transactions;''')
    cur.execute('''DROP TABLE IF EXISTS wallet;''')
    cur.execute('''DROP TABLE IF EXISTS users;''')
    cur.execute('''DROP TYPE IF EXISTS point_type;''')
    cur.execute('''
        CREATE TABLE users (
            id serial PRIMARY KEY UNIQUE,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
            )
    ;''')
    cur.execute('''CREATE TYPE point_type AS ENUM ('life', 'health', 'money');''')
    cur.execute('''
        CREATE TABLE transactions (
            id serial PRIMARY KEY UNIQUE,
            user_id integer,
            point_type point_type,
            val integer
            )
    ;''')
    cur.execute('''
        CREATE TABLE wallet (
            id serial PRIMARY KEY NOT NULL,
            user_id integer NOT NULL,
            username TEXT NOT NULL,
            health_points_balance integer,
            life_points_balance integer,
            money_points_balance integer,
            FOREIGN KEY (username) REFERENCES users (username),
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE (username, id)
            )
    ;''')

    seed_db(cur)
    conn.commit()
    close_db(conn, cur)

def seed_db(cur):
    """Seeds the database with a seed user and their wallet"""
    cur.execute('''
        INSERT INTO users (username, password, first_name, last_name)
        VALUES ('seed_user', %s, 'Seed', 'User')
        RETURNING id, username
        ;''', (generate_password_hash('password'),)
    )
    data = cur.fetchone()

    cur.execute('''
        INSERT INTO wallet (user_id, username, health_points_balance, life_points_balance, money_points_balance)
        VALUES (%s, %s, 0, 0, 0)
        ;''', (data[0], data[1],)
    )
    

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.cli.add_command(init_db_command)