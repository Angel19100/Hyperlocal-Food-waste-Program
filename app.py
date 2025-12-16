from flask import Flask, request, jsonify
from database import get_connection, initialize_database

app = Flask(__name__)

# Initialize database
initialize_database()


@app.route("/")
def home():
    return "Fresh-Share Network is running"


# ---------------- USERS ----------------

@app.route("/register", methods=["POST"])
def register_user():
    """
    Register a new user (Donor or Receiver)
    """
    data = request.json
    name = data.get("name")
    role = data.get("role")

    if role not in ["donor", "receiver"]:
        return jsonify({"error": "Invalid role"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, role) VALUES (?, ?)",
        (name, role)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "User registered successfully"})


# ---------------- FOOD ----------------

@app.route("/add_food", methods=["POST"])
def add_food():
    """
    Donor adds surplus food
    """
    data = request.json
    name = data.get("name")
    quantity = data.get("quantity")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO food (name, quantity, status) VALUES (?, ?, ?)",
        (name, quantity, "available")
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Food added successfully"})


@app.route("/food", methods=["GET"])
def view_food():
    """
    Receiver views available food
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM food WHERE status='available'")
    food_items = cursor.fetchall()

    conn.close()

    return jsonify(food_items)


@app.route("/claim/<int:food_id>", methods=["POST"])
def claim_food(food_id):
    """
    Receiver claims food
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE food SET status='claimed' WHERE id=? AND status='available'",
        (food_id,)
    )

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Food already claimed or not found"}), 400

    conn.commit()
    conn.close()

    return jsonify({"message": "Food claimed successfully"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
