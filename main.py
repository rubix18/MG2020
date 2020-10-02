"""
Example script utilising the db_client library. 
"""

from dbclient.dbclient import engine, ping_test, update, select_all

def main(): 
    truncate(engine)
    # ping_test(engine)

if __name__ == "__main__":
    main()