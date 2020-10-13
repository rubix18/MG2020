"""
Database client library - use these functions in your main code file by importing
this file, and then use these functions to input/output to DataBase. 
- Allows reading and writing to database defined in config.yml
"""

import yaml, socket, time, os
import pandas as pd
from sqlalchemy import create_engine


def init_conn(config):
    """
    Read local config file for database connection information and return connected database object
    """
    print(f'[DBCLIENT]: Config file - {config}')
    print(f'[DBCLIENT]: Reading URI from config file... ')
    with open(config) as file:
        conf = yaml.load(file, Loader=yaml.FullLoader)
        print(f'[DBCLIENT]: Database URI - {conf["URI"]}')
    print(f'[DBCLIENT]: Creating database engine...')
    engine = create_engine(conf['URI']) # Using sqlalchemy
    
    # Create schema if doesn't exist 
    stmt = """ CREATE TABLE IF NOT EXISTS public.events (
        id serial NOT NULL,
        src varchar(50) NOT NULL,
        src_loc varchar(50),
        ts timestamptz NULL DEFAULT clock_timestamp(),
        ball varchar(50) NULL,
        players varchar(50) NULL,
        CONSTRAINT events_pkey PRIMARY KEY (id)
        ); """
    with engine.connect() as con: 
        con.execute(stmt)
    print(f'[DBCLIENT]: Engine successfully created')
    return engine

def update(src_loc, ball_xy, players_xy, engine):
    
    if players_xy is None: 
        update_query = f"insert into events (src, src_loc, ball) values ('{socket.gethostname()}', '{src_loc}', '{ball_xy}');"
    elif ball_xy is None: 
        update_query = f"insert into events (src, src_loc, players) values ('{socket.gethostname()}', '{src_loc}', '{players_xy}');"
    else: 
        update_query = f"insert into events (src, src_loc, ball, players) values ('{socket.gethostname()}', '{src_loc}', '{ball_xy}', '{players_xy}');"
    
    with engine.connect() as con:
        result = con.execute(update_query)

def select_all(table_name, engine):
    """
    Returns dataframe of specified table
    """
    query = f'select * from {table_name}'
    result = pd.read_sql_query(query, engine) # Using pandas 
    return result

def ping_test(engine): 
    """
    For testing purposes: Continuously insert into database every 1 second
    """
    while True:
        update('right corner', [1, 2], [[3, 4], [30, 40], [32, 10]], engine)
        print(select_all('events', engine))
        time.sleep(1)

def truncate(engine):
    """
    Clears all table values
    """
    print(f'[DBCLIENT]: Truncating events table...')
    stmt = f'truncate table events'
    with engine.connect() as con: 
        con.execute(stmt)
    print('[DBCLIENT]: Reading events table: ')
    print(select_all('events', engine))

dir_path = os.path.dirname(os.path.realpath(__file__))
engine = init_conn(f'{dir_path}/config/config.yml')

if __name__ == "__main__":
    pass