from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# --- 1. Database Configuration ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'db.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- 2. Database Model ---
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    is_completed = db.Column(db.Boolean, default=False)

# --- 3. API Routes ---

# Home Route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to your Flask To-Do API"})

# GET: Fetch all tasks
@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    result = []
    for todo in todos:
        result.append({
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "is_completed": todo.is_completed
        })
    return jsonify(result)

# POST: Create a new task
@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
        
    new_todo = Todo(
        title=data['title'],
        description=data.get('description', '')
    )
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({"message": "Task created successfully!", "id": new_todo.id}), 201

# DELETE: Remove a specific task by ID
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({"message": "Task not found"}), 404
    
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": f"Task {todo_id} deleted successfully"}), 200

# --- 4. Server Execution ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Generates the db.sqlite file
    app.run(debug=True)
