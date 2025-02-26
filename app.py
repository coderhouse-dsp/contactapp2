from flask import Flask, render_template, request
import pyodbc
from config import CONNECTION_STRING

app = Flask(__name__)

# Establish connection using the environment variable
conn = pyodbc.connect(CONNECTION_STRING)
cursor = conn.cursor()

# Ensure table exists
cursor.execute("""
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
    CREATE TABLE users (
        id INT PRIMARY KEY IDENTITY(1,1),
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL
    )
""")
conn.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    return render_template("index.html", users=users)

if __name__ == "__main__":
    app.run(debug=True)
