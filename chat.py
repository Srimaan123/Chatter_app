from flask import Flask,render_template,redirect,url_for,Blueprint,request,session
import sqlite3
from flask_socketio import SocketIO, join_room, emit

socketio = SocketIO()

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
  print(user_id) 
  db = get()
  cur = db.cursor()
  
  if request.method == "GET":
    cur.execute("SELECT * FROM chats WHERE (user_id=? AND reciever_id=?) OR (user_id=? AND  reciever_id=?)",(user_id,reciever_id,reciever_id,user_id))
    chats = cur.fetchall()
    db.close()
    return render_template("chat.html",chats=chats,user_id=user_id,reciever_id=reciever_id)
  
# 🔹 join room
@socketio.on("join_chat")
def join_chat(data):
    user_id = data["user_id"]
    reciever_id = data["reciever_id"]

    room = f"{min(user_id, reciever_id)}_{max(user_id, reciever_id)}"
    join_room(room)

    print("Joined room:", room)


# 🔹 send message
@socketio.on("send_message")
def handle_message(data):
    user_id = data["user_id"]
    reciever_id = data["reciever_id"]
    msg = data["message"]

    db = get()
    cur = db.cursor()

    # save to DB (same as your old code)
    cur.execute(
        "INSERT INTO chats(user_id, reciever_id, post) VALUES(?,?,?)",
        (user_id, reciever_id, msg)
    )
    db.commit()
    db.close()

    room = f"{min(user_id, reciever_id)}_{max(user_id, reciever_id)}"

    emit("receive_message", data, room=room)
