from flask import Flask,render_template,request,redirect,Blueprint,session,url_for
import sqlite3
contacts_bp = Blueprint("contacts",__name__)

def get():
  return sqlite3.connect("data.db")

db = get()
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS contacts(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
name TEXT,
phone TEXT
)
""")
db.commit()
db.close()

@contacts_bp.route("/contacts",methods=["GET","POST"])
def contacts():
  db = get()
  cur = db.cursor()
  if request.method == "GET":
    user_id  = session.get("user_id")
    cur.execute("SELECT *  FROM contacts WHERE user_id=?",(user_id,))
    contacts = cur.fetchall()
    return render_template("contacts.html",contacts=contacts)
  if request.method == 'POST':
    reciever_phone = request.form.get("phone")
    cur.execute("SELECT id FROM users WHERE phone=?",(reciever_phone,))
    row = cur.fetchone()
    reciever_id = row[0]
    print(f"reciever_id:{reciever_id}")
    if reciever_id:
      return redirect(url_for("chat.chat",reciever_id=reciever_id))
    else:
      return "go you hacker!!!!"
   
@contacts_bp.route("/add_contact",methods=["GET","POST"])
def add_contact():
  db = get()
  cur = db.cursor()
  if request.method == "GET":
    return render_template("add_contact.html")
  if request.method == "POST":
    name = request.form.get("name")
    phone = request.form.get("phone")
    user_id = session.get("user_id")
    cur.execute("SELECT *  FROM users WHERE phone=?",(phone,))
    reciever = cur.fetchone()
    if reciever:
      cur.execute("INSERT INTO contacts(user_id,name,phone) VALUES(?,?,?)",(user_id,name,phone))
    else:
      return "the person does not exist in app"
    db.commit()
    db.close()
    return redirect(url_for("contacts.contacts"))