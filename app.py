from flask import Flask, request, jsonify, render_template
from datetime import datetime
import random
import string

app = Flask(__name__)

# In-memory user storage
users = []

def generate_random_user():
    name = ''.join(random.choices(string.ascii_letters, k=6)).capitalize()
    email = f"{name.lower()}@example.com"
    status = random.choice(["Active", "Inactive"])
    return {
        "id": len(users) + 1,
        "name": name,
        "email": email,
        "status": status,
        "joined": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.json
    new_user = {
        "id": len(users) + 1,
        "name": data["name"],
        "email": data["email"],
        "status": "Active",
        "joined": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    users.append(new_user)
    return jsonify(new_user), 201

@app.route('/api/users/random', methods=['POST'])
def add_random_user():
    user = generate_random_user()
    users.append(user)
    return jsonify(user), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    for user in users:
        if user["id"] == user_id:
            user.update(request.json)
            return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/api/users/<int:user_id>/toggle_status', methods=['PATCH'])
def toggle_status(user_id):
    for user in users:
        if user["id"] == user_id:
            user["status"] = "Inactive" if user["status"] == "Active" else "Active"
            return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [user for user in users if user["id"] != user_id]
    return jsonify({"message": "User deleted"})

@app.route('/api/stats', methods=['GET'])
def user_stats():
    total = len(users)
    active = sum(1 for u in users if u["status"] == "Active")
    inactive = total - active
    return jsonify({
        "total": total,
        "active": active,
        "inactive": inactive
    })

if __name__ == '__main__':
    app.run(debug=True)
