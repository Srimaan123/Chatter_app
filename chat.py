from flask import Flask,render_template,redirect,url_for,Blueprint,request,session
import sqlite3

chat_bp = Blueprint("chat",__name__)

def get():
  return sqlite3.connect("data.db")
  
db = get()
cur = db.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS chats(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  reciever_id INTEGER,
  post TEXT
)""")
db.commit()
db.close()
  
@chat_bp.route("/chat/<int:reciever_id>",methods = ["GET","POST"])
def chat(reciever_id):
  user_id = session.get("user_id")
  db = get()
  cur = db.cursor()
  
  if request.method == "GET":
    cur.execute("SELECT * FROM chats WHERE (user_id=? AND reciever_id=?) OR (user_id=? AND  reciever_id=?)",(user_id,reciever_id,reciever_id,user_id))
    chats = cur.fetchall()
    db.close()
    return render_template("chat.html",chats=chats,user_id=user_id,reciever_id=reciever_id)
  if request.method == "POST":
    clicked_button = request.form.get("button")
    if clicked_button == "exit":
      db.close()
      return redirect(url_for("contacts.contacts"))
    if clicked_button == "send":
      post = request.form.get("post")
      cur.execute("INSERT INTO chats(user_id,reciever_id,post) VALUES(?,?,?)",(user_id,reciever_id,post))
      db.commit()
      db.close()
      return redirect(url_for("chat.chat",reciever_id=reciever_id))