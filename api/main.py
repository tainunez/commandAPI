from flask import Flask, jsonify, request
from db import get_commands, add_commands, open_connection
app = Flask(__name__)

#old flask syntax, just use @app.<HTTP METHOD> with no methods arguments in future 
@app.route('/', methods=['POST', 'GET'])
def commands():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400

        add_commands(request.get_json())
        return 'Command has been added to the db'

    return get_commands()

#get all commands from db
@app.get('/commands')
def get_all_commands():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM commands')
        commands = cursor.fetchall()
        if result > 0:
            got_commands = jsonify(commands)
        else:
            got_commands = jsonify({"message": "no commands were found..."})
    conn.close()
    return got_commands

@app.get('/commands/command_id')
def get_command():
    conn = open_connection
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM commands WHERE command_id IN LIMIT 1')


#create a new command and add to db
@app.post('/commands')
def add_command(command):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO commands (command, guide, platform) VALUES  (%s, %s, %s)', (command["command"], command["guide"], command["platform"]))





if __name__ == '__main__':
  app.run(debug=True)