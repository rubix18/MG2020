"""
Database client library - use these functions in your main code file by importing
this file, and then use these functions to input/output to DataBase. 
- Allows reading and writing to database defined in config.yml
"""

import yaml, socket, time, os, requests
import pandas as pd
from sqlalchemy import create_engine


def init_conn(config):
    """
    Read local config file for database connection information and return connected database object
    """
    print(f'[DBCLIENT]: Config file - {config}')
    print(f'[DBCLIENT]: Reading URI from config file... ')
    with open(config) as file:
        global conf 
        conf = yaml.load(file, Loader=yaml.FullLoader)
        print(f'[DBCLIENT]: Database URI - {conf["URI"]}')
        print(f'[DBCLIENT]: Server URL - {conf["URL"]}')
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
        ); 
        
        CREATE TABLE IF NOT EXISTS public.flags (
        hostname varchar(50) NOT NULL,
        replay boolean default false,
        CONSTRAINT flags_pkey PRIMARY KEY (hostname)
        );
        """
    with engine.connect() as con: 
        con.execute(stmt)

    # Check if flags table has this pi's (the pi running this script) hostname, if not, insert it. 
    stmt = f"select count(*) from flags where hostname = '{socket.gethostname()}'"
    exists = int(pd.read_sql_query(stmt, engine).iloc[0]) # Using pandas 
    if not exists: 
        stmt = f"insert into flags (hostname) values ('{socket.gethostname()}');"
        with engine.connect() as con: 
            con.execute(stmt)
        print(f'[DBCLIENT]: Registered {socket.gethostname()} into flags table')

    # Reset all replay flags to 0 
    stmt = f"update flags set replay = false;"
    with engine.connect() as con: 
        con.execute(stmt)

    print(f'[DBCLIENT]: Database successfully connected and initialised')
    return engine

def update(src_loc, ball_xy, players_xy):
    
    if players_xy is None: 
        update_query = f"insert into events (src, src_loc, ball) values ('{socket.gethostname()}', '{src_loc}', '{ball_xy}');"
    elif ball_xy is None: 
        update_query = f"insert into events (src, src_loc, players) values ('{socket.gethostname()}', '{src_loc}', '{players_xy}');"
    else: 
        update_query = f"insert into events (src, src_loc, ball, players) values ('{socket.gethostname()}', '{src_loc}', '{ball_xy}', '{players_xy}');"
    
    with engine.connect() as con:
        result = con.execute(update_query)

def select_all(table_name):
    """
    Returns dataframe of specified table
    """
    query = f'select * from {table_name}'
    result = pd.read_sql_query(query, engine) # Using pandas 
    return result

def ping_test(): 
    """
    For testing purposes: Continuously insert into database every 1 second
    """
    while True:
        update('right corner', [1, 2], [[3, 4], [30, 40], [32, 10]], engine)
        print(select_all('events', engine))
        time.sleep(1)

def truncate():
    """
    Clears all table values
    """
    print(f'[DBCLIENT]: Truncating events table...')
    stmt = f'truncate table events'
    with engine.connect() as con: 
        con.execute(stmt)
    print('[DBCLIENT]: Reading events table: ')
    print(select_all('events', engine))

def replay_requested(hostname=socket.gethostname()):
    """
    Queries database to see if there is an outstanding flag toggled by server for replay video to be sent. 
    Returns 0 or 1
    """
    query = f"select replay from flags where hostname = '{hostname}';"
    result = pd.read_sql_query(query, engine).bool()
    return result 

def send_replay(file):
    files = {'file': (f'{socket.gethostname()}.mp4', file)}
    url = conf['URL'] + '/upload'
    x = requests.post(url, files = files)
    print('[DBCLIENT]: Sent file to server ', x)
    # after sending the file, reset the pi's own flag to 0 
    stmt = f"update flags set replay = false where hostname = '{socket.gethostname()}';"
    with engine.connect() as con: 
        con.execute(stmt)
    print(f'[DBCLIENT]: Reset replay requested flag for {socket.gethostname()}')

def get_hostnames():
    query = "select distinct hostname from flags;"
    result = list(pd.read_sql_query(query, engine)['hostname'])
    return result

def request_replay(hostname):
    stmt = f"update flags set replay = true where hostname = '{hostname}'"
    with engine.connect() as con: 
        con.execute(stmt)
    print(f'[DBCLIENT]: Set replay requested flag for {socket.gethostname()}')

def wait(hostname):
    timeout_count = 1
    while True: 
        if not replay_requested(hostname):
            return True 
        print(f'[DBCLIENT]: Waiting for replay file to be sent from {hostname}')
        time.sleep(1)
        timeout_count += 1 
        if timeout_count > 5: 
            print(f'[DBCLIENT]: TIMEOUT from {hostname} OCCURRED')
            return False 


dir_path = os.path.dirname(os.path.realpath(__file__))
engine = init_conn(f'{dir_path}/config/config.yml')

if __name__ == "__main__":
    # request_replay('kk-XPS-15-9570')
    # wait('kk-XPS-15-9570')
    file = open('replay.mp4', 'rb')
    send_replay(file)
    # while True: 
    #     time.sleep(1)
    #     print(replay_requested())
    