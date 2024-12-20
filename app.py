import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
from validations import is_valid_datetime, is_valid_priority, is_valid_status

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Configure MongoDB
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)
  
# Home Route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Todo Flask API with MongoDB!"})

# Create a new document
@app.route('/addTodo', methods=['POST'])
def add_todo():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    if 'title' not in data or not data['title']:
        return jsonify({"error": "Title is required"}), 400

    if 'description' not in data or not data['description']:
        return jsonify({"error": "Description is required"}), 400
    
    if 'priority' not in data or not is_valid_priority(data['priority']):
        return jsonify({"error": "Invalid or missing priority. Allowed values: 'low', 'medium', 'high'"}), 400
    
    if 'status' not in data or not is_valid_status(data['status']):
        return jsonify({"error": "Invalid or missing status. Allowed values: 'pending', 'in_progress', 'completed', 'archived'"}), 400
    
    # Validate required fields and their values
    if 'datetime' not in data or not is_valid_datetime(data['datetime']):
        return jsonify({"error": "Invalid or missing datetime. Expected format: YYYY-MM-DD HH:MM:SS"}), 400

    inserted_id = mongo.db.todos.insert_one(data).inserted_id
    return jsonify({"message": "Todo's added successfully!", "id": str(inserted_id)}), 201

# Get all documents
@app.route('/todos', methods=['GET'])
def get_documents():
    documents = mongo.db.todos.find()
    result = []
    for doc in documents:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        result.append(doc)
    return jsonify(result), 200

# Get a single document by ID
@app.route('/todo/<id>', methods=['GET'])
def get_document(id):
    try:
        document = mongo.db.todos.find_one({"_id": ObjectId(id)})
        if not document:
            return jsonify({"error": "Todo not found"}), 404
        document["_id"] = str(document["_id"])
        return jsonify(document), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Update a document by ID
@app.route('/updateTodo/<id>', methods=['PUT'])
def update_document(id):
    data = request.json

    # Validations
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if 'title' not in data or not data['title']:
        return jsonify({"error": "Title is required"}), 400

    if 'description' not in data or not data['description']:
        return jsonify({"error": "Description is required"}), 400
    
    if 'priority' not in data or not is_valid_priority(data['priority']):
        return jsonify({"error": "Invalid or missing priority. Allowed values: 'low', 'medium', 'high'"}), 400
    
    if 'status' not in data or not is_valid_status(data['status']):
        return jsonify({"error": "Invalid or missing status. Allowed values: 'pending', 'in_progress', 'completed', 'archived'"}), 400
    
    # Validate required fields and their values
    if 'datetime' not in data or not is_valid_datetime(data['datetime']):
        return jsonify({"error": "Invalid or missing datetime. Expected format: YYYY-MM-DD HH:MM:SS"}), 400

    try:
        result = mongo.db.todos.replace_one({"_id": ObjectId(id)}, data)
        if result.matched_count == 0:
            return jsonify({"error": "Todo not found"}), 404
        return jsonify({"message": "Todo updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Update only specific field example-(status) 
@app.route('/updateTodo/<id>', methods=['PATCH'])
def patch_document(id):
    try:
        # Validate the ObjectId
        if not ObjectId.is_valid(id):
            return jsonify({"error": "Invalid ID format"}), 400

        # Get the update fields from the request body
        update_data = request.json
        if not update_data:
            return jsonify({"error": "No data provided for update"}), 400

        # Perform the update
        result = mongo.db.todos.update_one({"_id": ObjectId(id)}, {"$set": update_data})

        # Check if the document was modified
        if result.matched_count == 0:
            return jsonify({"error": "Document not found"}), 404

        if result.modified_count == 0:
            return jsonify({"message": "No changes made to the document"}), 200

        return jsonify({"message": "Document updated successfully"}), 200
    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

# Delete a document by ID
@app.route('/deleteTodo/<id>', methods=['DELETE'])
def delete_document(id):
    try:
        result = mongo.db.todos.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Todo not found"}), 404
        return jsonify({"message": "Todo deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)