from flask import Flask,Blueprint,url_for,request,render_template,redirect,session
import sqlite3
auth_bp = Blueprint("auth", __name__)

def get():
  return sqlite3.connect("data.db")
db = get()
cur = db.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT,
  password TEXT,
  phone TEXT
)
""")
db.commit()
db.close()

@auth_bp.route("/",methods=["GET","POST"])
def login():
  db = get()
  cur = db.cursor()
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")
    phone = request.form.get("phone")
    cur.execute("SELECT *  FROM users WHERE username=? AND password=? AND phone=?",(username,password,phone))
    user = cur.fetchall()
    db.close()
    if user == []:
      return f'<h1>invalid credentials</h1><a href="{url_for("auth.login")}">try again</a>'
    session.clear()
    single_user = user[0]
    session["user_id"] = single_user[0]
    return redirect(url_for("contacts.contacts"))
  else:
    return render_template("login.html")
            
@auth_bp.route("/add_account",methods=["GET","POST"])
def add_account():
  db = get()
  cur = db.cursor()
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")
    phone = request.form.get("phone")
    cur.execute("INSERT INTO users(username,password,phone) VALUES(?,?,?)",(username,password,phone))
    db.commit()
    db.close()
    return redirect(url_for("auth.login"))
  else:
    return render_template("add_account.html")
