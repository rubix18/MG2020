## Section 1. 
# Set up the Raspberry Pi for PostgreSQL database by following this tutorial:
# THIS IS ONLY REQUIRED IF YOU WANT TO HOST THE DATABASE SERVER ON YOUR PI
# IF YOU ONLY WANT TO CONNECT, READ AND WRITE TO DATABASE, SKIP TO NEXT SECTION

https://opensource.com/article/17/10/set-postgres-database-your-raspberry-pi

Overview: 
1. Install Postgres and required packages
2. Create new database user
3. Create database
4. Edit config files to allow remote connections
5. Restart postgres database service
6. Connect from remote computer (using DBeaver, PgAdmin, or Python)


## Section 2. Setting up client Pi configuration. 

To connect to the database, you will need to know: 
1. Databse username and password 
2. IP Address and port 
3. Database name

Put these details in database_module/config/config.yml file (make one if not there) in the form: 

*** config.yml *** 
URI: postgresql://username:password@ipaddress:port/databasename

E.g.
URI: postgresql://john:Password@192.168.1.113:5432/testdb


# Section 3. Setting up client Pi python environment/required libraries

1. Create a virtual environment: python3 -m venv venv
2. Activate virtual environment: source venv/bin/activate
3. Install required libraries: pip install -r requirements.txt
        

# Section 4. Using the script

