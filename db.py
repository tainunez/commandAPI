import os
import pymysql
from flask import jsonify

#retrieve the database credentials 
db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

#connect to the mysql database using the credentials above
def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    try:
        if os.environ.get("GAE_ENV") == 'standard':
            conn = pymysql.connect(user=db_user, 
                                   password=db_password,
                                   unix_socket=unix_socket, 
                                   db=db_name, 
                                   cursorclass=pymysql.cursors.DictCursor)
    except pymysql.MySQLError as e:
        print(e)
    return conn

#get all commands currently in the db
def get_commands():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM commands')
        commands = cursor.fetchall()
        if result > 0:
            got_commands = jsonify(commands)
        else:
            got_commands = 'No commands in DB'
    conn.close()
    return got_commands

#add a new command to the db by inserting into table
def add_commands(command):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO commands (command, guide, platform) VALUES  (%s, %s, %s)', (command["command"], command["guide"], command["platform"]))
    conn.commit()
    conn.close()

