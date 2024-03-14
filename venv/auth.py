from flask import Flask, render_template, request, redirect, flash, url_for, session
from helpers import apology
import sqlite3

 
auth = Flask(__name__)
auth.secret_key = "CarbonFootprint"
auth.config["SECURITY_KEY"] = "your_security_key"
auth.config["FLASK_FLASH_MESSAGES"] = {
    "success": "alert-success",
    "error": "alert-error"
}

DATABASE = 'database.db'

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT, email TEXT, password TEXT, confirmpassword TEXT)''')
    
    conn.commit()
    conn.close()
    
def insert_user(name, email, password, confirmpassword):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users(name, email, password, confirmpassword) VALUES(?, ?, ?, ?)", (name, email, password, confirmpassword))
    conn.commit()
    conn.close()
    
    
def get_user(name, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = ? AND password = ?", (name, password))
    user = cursor.fetchone()
    conn.close
    return user
    
create_table()    


@auth.route("/")
def home():
    
    return render_template('home.html')

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmpassword")
        
        if password != confirm_password:
            flash("Your password does not match")
        
        insert_user(name, email, password, confirm_password)
        return redirect("/login")
    else:
        return render_template("signup.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        user = get_user(name, password)
        if user:
            session["name"] = name
            return redirect(f"http://localhost:8501?user_name={name.split()[0]}")
        
        else:
            flash("Incorrect name or password", category="error")
        
    return render_template("login.html")

@auth.route("/logout")
def logout():
    return redirect("/")

@auth.route("/home")
def index():
    return render_template("home.html")


if __name__ == "__main__":
    auth.run(debug=True)