from flask import Flask, request
from flask import render_template
from flask import redirect
from flask_login.mixins import UserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


class Task(db.Model):
   # __tablename__ = 'Task'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    doing = db.Column(db.Boolean, default=False)
    done = db.Column(db.Boolean, default=False)

    def __init__(self, content):
        self.content = content
        self.done = False
        self.doing = False

    def __repr__(self):
        return "<Content %s>" % self.content

# class User(UserMixin,db.Model):
#     __tablename__ ='User'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(200))
#     password = db.Column(db.String(200))
#     def __repr__(self):
#         return "<Username: {}>".format(self.username)

db.create_all()
db.session.commit()

@app.route("/")
def login():
    return redirect("/home")


@app.route("/home")
def tasks_list():
    tasks = Task.query.all()
    return render_template("list.html", tasks=tasks)


@app.route("/task", methods=["POST"])
def add_task():
    content = request.form["content"]
    if not content:
        return "Error"

    task = Task(content)
    db.session.add(task)
    db.session.commit()
    return redirect("/home")


@app.route("/doing/<int:task_id>")
def doingnow(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect("/home")
    if task.doing:
        task.doing = False
    else:
        task.doing = True
    if task.done:
        task.done = False
    db.session.commit()
    return redirect("/home")


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect("/home")

    db.session.delete(task)
    db.session.commit()
    return redirect("/home")


@app.route("/done/<int:task_id>")
def resolve_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return redirect("/")
    if task.done:
        task.done = False
    else:
        task.done = True
    if task.doing:
        task.doing=False

    db.session.commit()
    return redirect("/home")


if __name__ == "__main__":
    app.run(debug=True)