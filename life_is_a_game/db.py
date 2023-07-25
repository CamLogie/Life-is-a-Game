import click
import psycopg2
import os

from flask import current_app, g

def get_db():
    conn = psycopg2.connect(
        host="localhost",
        database="life_is_a_game_db",
        user=os.environ["DATABASE_USER"],
        password=os.environ["DATABASE_PASSWORD"]
    )
    return conn

def close_db():
    conn = get_db()

    conn.close()

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS transactions')
    cur.execute('DROP TABLE IF EXISTS balances')
    cur.execute('DROP TABLE IF EXISTS users')
    cur.execute('CREATE TABLE users (id serial PRIMARY KEY UNIQUE,'
                                    'first_name varchar (30) NOT NULL,'
                                    'last_name varchar (30) NOT NULL,'
                                    'username varchar (30) NOT NULL UNIQUE,'
                                    'password varchar (50) NOT NULL);'
                                    )
    cur.execute('CREATE TYPE point_type AS ENUM (\'life\', \'health\', \'money\')')
    cur.execute('CREATE TABLE transactions (id serial PRIMARY KEY UNIQUE,'
                'user_id integer,'
                'point_type point_type,'
                'val integer);'
                )
    cur.execute('CREATE TABLE balances (id serial PRIMARY KEY,'
                'username varchar (30),'
                'health_points_balance integer,'
                'life_points_balance integer,'
                'money_points_balance integer,'
                'FOREIGN KEY (username) REFERENCES users (username),'
                'FOREIGN KEY (id) REFERENCES users (id),'
                'UNIQUE (username, id));'
                )

    conn.commit()
    cur.close()

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.cli.add_command(init_db_command)
    close_db()