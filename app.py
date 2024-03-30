from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

##############STEPS TO DB CRERATION############
""" 
flask shell
import db ##the object## from our app
write db.create_all()
exit the python terminal
"""
##############STEPS TO DB CRERATION############

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f'<Task {self.id}>'



@app.route('/', methods=['POST','GET'])
def index():
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>', methods=['POST','GET'])
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleted that task"
    

@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        task_to_update = Todo.query.get_or_404(id)

        try:
            task.content = request.form['content']

            try:
                db.session.commit()
                return redirect('/')
            except:
                return "There was a problem updating that task"

        except:
            return "There was a problem updating that task"
    else:
        
        return render_template('update.html',task = task)

if __name__ == '__main__':
    app.run(debug=True) 