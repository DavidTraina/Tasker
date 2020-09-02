from flask import Flask, render_template, request, redirect
from collections import OrderedDict
import uuid, datetime

app = Flask(__name__)

db = OrderedDict()


class Task():
    def __init__(self, content, date_created):
        self.content = content
        self.date_created = date_created

    def __repr__(self):
        return "content={}, created={}".format(self.content, self.date_created)


@app.route('/', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        task_content = request.form['content']  # 'content' refers to name of text input in form in index.html
        task_id = uuid.uuid4()
        new_task = Task(task_content,
                        datetime.datetime.now(tz=datetime.timezone.utc))
        db[task_id] = new_task
        return redirect('/')
    return render_template('index.html', tasks=db.items())


@app.route('/delete/<uuid:task_id>')
def delete(task_id):
    return redirect('/') if db.pop(task_id, None) is not None else 'OOoooOOooOooooOOOOOOoooOOOps'


@app.route('/edit/<uuid:task_id>', methods=['POST', 'GET'])
def edit(task_id):
    task_to_edit = db.get(task_id, None)
    if task_to_edit is None:
        return 'OOoooOOooOooooOOOOOOoooOOOps'
    if request.method == 'POST':
        task_to_edit.content = request.form['content']
        return redirect('/')
    return render_template('edit.html', task_id=task_id, task=task_to_edit)


if __name__ == '__main__':
    app.run(debug=True)
