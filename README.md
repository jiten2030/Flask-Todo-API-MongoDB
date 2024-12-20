# Flask Todo API with MongoDB

This is a simple Flask-based REST API for managing a Todo list. The API integrates with MongoDB to perform CRUD (Create, Read, Update, Delete) operations. It also includes validations for various fields.

## Features
- **Get all todos**: Retrieve a list of all todos.
- **Get a single todo**: Retrieve details of a specific todo by its ID.
- **Create a todo**: Add a new todo with required fields.
- **Update a todo**: Update all fields of a specific todo by its ID.
- **Patch update a todo**: Update specific fields of a todo by its ID.
- **Delete a todo**: Remove a todo by its ID.

## Prerequisites

- Python 3.7+
- MongoDB

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jiten2030/Flask-Todo-API-MongoDB.git
   cd Flask-Todo-API-MongoDB
   ```
2. Open the folder in VS Code or other editior:
   ```bash
   code . # You can also open this folder manually
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up MongoDB and configure the connection URI in `.env` file:
   ```env
   MONGO_URI=mongodb://localhost:27017/todoDB
   ```
5. Start the server:
   ```bash
   python app.py
   ```

## API Endpoints

### 1. Get All Todos
**Endpoint:** `GET /todos`

**Description:** Retrieves all todos from the database.

**Response:**
```json
[
  {
    "_id": "<id>",
    "title": "Task 1",
    "description": "Description for Task 1",
    "status": "pending",
    "priority": "high",
    "datetime": "2024-12-20 12:00:00"
  }
]
```

### 2. Get a Single Todo
**Endpoint:** `GET /todo/<id>`

**Description:** Retrieves a specific todo by its ID.

**Response:**
```json
{
  "_id": "<id>",
  "title": "Task 1",
  "description": "Description for Task 1",
  "status": "pending",
  "priority": "high",
  "datetime": "2024-12-20 12:00:00"
}
```

### 3. Create a Todo
**Endpoint:** `POST /todo`

**Description:** Adds a new todo to the database.

**Request Body:**
```json
{
  "title": "Task 1",
  "description": "Description for Task 1",
  "status": "pending",
  "priority": "medium",
  "datetime": "2024-12-20 12:00:00"
}
```

**Validation Rules:**
- `title`: Required
- `description`: Required
- `status`: Must be one of `pending`, `in_progress`, `completed`, `archived`
- `priority`: Must be one of `low`, `medium`, `high`
- `datetime`: Must be in the format `YYYY-MM-DD HH:MM:SS`

**Response:**
```json
{
  "message": "Todo created successfully",
  "todo": {
    "_id": "<id>",
    "title": "Task 1",
    "description": "Description for Task 1",
    "status": "pending",
    "priority": "medium",
    "datetime": "2024-12-20 12:00:00"
  }
}
```

### 4. Update a Todo (Full Update)
**Endpoint:** `PUT /todo/<id>`

**Description:** Updates all fields of a specific todo by its ID.

**Request Body:**
```json
{
  "title": "Updated Task",
  "description": "Updated description",
  "status": "completed",
  "priority": "high",
  "datetime": "2024-12-21 15:00:00"
}
```

**Response:**
```json
{
  "message": "Todo updated successfully",
  "todo": {
    "_id": "<id>",
    "title": "Updated Task",
    "description": "Updated description",
    "status": "completed",
    "priority": "high",
    "datetime": "2024-12-21 15:00:00"
  }
}
```

### 5. Patch Update a Todo
**Endpoint:** `PATCH /todo/<id>`

**Description:** Updates specific fields of a todo by its ID.

**Request Body:**
```json
{
  "status": "in_progress"
}
```

**Response:**
```json
{
  "message": "Todo updated successfully",
  "todo": {
    "_id": "<id>",
    "status": "in_progress"
  }
}
```

### 6. Delete a Todo
**Endpoint:** `DELETE /todo/<id>`

**Description:** Deletes a specific todo by its ID.

**Response:**
```json
{
  "message": "Todo deleted successfully"
}
```

## Validation
Field validation is performed using Flask and ensures:
- `title` and `description` are required fields.
- `status` must be one of: `pending`, `in_progress`, `completed`, `archived`.
- `priority` must be one of: `low`, `medium`, `high`.
- `datetime` must follow the format `YYYY-MM-DD HH:MM:SS`.

## Running Tests
To test the API locally using `http://localhost:5000/`, you can run the following commands for the respective endpoints.
