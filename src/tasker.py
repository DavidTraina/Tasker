from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime
import os

app = Flask(__name__)


def get_env_var(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        raise Exception(
            "environment variable {} should be set but isn't".format(var_name)
        )


POSTGRES_URL = get_env_var("POSTGRES_URL")
POSTGRES_USER = get_env_var("POSTGRES_USER")
POSTGRES_PASSWORD = get_env_var("POSTGRES_PASSWORD")
POSTGRES_DB = get_env_var("POSTGRES_DB")
DB_URL = "postgresql+psycopg2://{user}:{pw}@{url}/{db}".format(
    user=POSTGRES_USER, pw=POSTGRES_PASSWORD, url=POSTGRES_URL, db=POSTGRES_DB
)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # silence the deprecation warning

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    content = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return "<Task %s>" % self.id

    # def __repr__(self):
    #     return "id={}, content={}, created={}".format(self.id, self.content, self.date_created)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        task_content = request.form[
            "content"
        ]  # 'content' refers to name of text input in form in index.html
        new_task = Task(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "OOoooOOooOooooOOOOOOoooOOOps"
    return render_template(
        "index.html", tasks=Task.query.order_by(Task.date_created).all()
    )


@app.route("/delete/<uuid:task_id>")
def delete(task_id):
    task_to_del = Task.query.get_or_404(task_id)
    try:
        db.session.delete(task_to_del)
        db.session.commit()
        return redirect("/")
    except:
        return "OOoooOOooOooooOOOOOOoooOOOps"


@app.route("/edit/<uuid:task_id>", methods=["POST", "GET"])
def edit(task_id):
    task_to_edit = Task.query.get_or_404(task_id)
    if request.method == "POST":
        task_to_edit.content = request.form["content"]
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "OOoooOOooOooooOOOOOOoooOOOps"
    return render_template("edit.html", task=task_to_edit)


if __name__ == "__main__":
    db.create_all()
    app.run(
        host="0.0.0.0", port=5000, debug=True
    )  # todo: have to use 0.0.0.0 instead of localhost for reasons I don't fully understand
