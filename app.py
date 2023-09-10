from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# SQLite database setup
conn = sqlite3.connect('todo.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS todos
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              description TEXT NOT NULL)''')
conn.commit()

def row_to_dict(row):
    return {'id': row[0], 'description': row[2], 'title': row[1]}

#create new todo item
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not title or not description:
        return jsonify({'error': 'Title and description are required'}), 400

    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("INSERT INTO todos (title, description) VALUES (?, ?)", (title, description))
    conn.commit()

    return jsonify({'message': 'Todo created successfully'}), 201

#retrieve list of all todo items
@app.route('/todos', methods=['GET'])
def get_todos():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT * FROM todos ORDER BY id ASC")
    todos = [row_to_dict(row) for row in c.fetchall()]
    conn.close()

    return jsonify(todos)

#retrieve single todo item by ID
@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    todo = c.fetchone()
    conn.close()

    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    return jsonify(row_to_dict(todo))

#update a todo item
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    todo = c.fetchone()

    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    if title:
        c.execute("UPDATE todos SET title = ? WHERE id = ?", (title, todo_id))
    if description:
        c.execute("UPDATE todos SET description = ? WHERE id = ?", (description, todo_id))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Todo updated successfully'})

#delete a todo item
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    todo = c.fetchone()

    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    c.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Todo deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
