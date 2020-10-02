"""
Example script utilising the db_client library. 
"""

from dbclient.dbclient import (
    engine,     # database object
    # functions
    ping_test,  # usage: ping_test(engine)
    update,     # usage: update(src_loc, ball_xy, players_xy, engine)
    select_all  # usage: select_all(table_name, engine)
)

def main(): 
    ping_test(engine)

if __name__ == "__main__":
    main()