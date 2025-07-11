from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Настройка базы данных
db = SQLAlchemy(app)

# модель задачи(таблица Task)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codename = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(10), nullable=True)
    email = db.Column(db.String(10), nullable=True)
    access_level = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return f"<Task {self.title}>"


with app.app_context():
    db.create_all()


@app.route('/')
@app.route('/tasks')
def get_tasks():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)


@app.route('/info/<int:id>')
def get_infos():
    # infos = Task.query.all()
    # return render_template('infos.html', infos=infos)
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('get_tasks'))


@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        codename = request.form['codename']
        contact = request.form['contact']
        email = request.form['email']
        access_level = request.form['access_level']
        if codename.strip():
            new_task = Task(codename=codename, contact=contact,
                            email=email, access_level=access_level)
            db.session.add(new_task)
            db.session.commit()
        return redirect(url_for('get_tasks'))
    return render_template('add_task.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        new_codename = request.form['codename']
        new_contact = request.form['contact']
        new_email = request.form['email']
        new_access_level = request.form['access_level']
        if new_codename.strip():
            task.codename = new_codename
            task.contact = new_contact
            task.email = new_email
            task.access_level = new_access_level
            db.session.commit()
        return redirect(url_for('get_tasks'))
    return render_template('edit_task.html', task=task)


@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('get_tasks'))


if __name__ == "__main__":
    app.run(debug=True)
