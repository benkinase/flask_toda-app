from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask-crud.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

#Add route
@app.route('/', methods=['POST','GET'])
def index():
    #post request
    if request.method=='POST':
       task_content = request.form['task']
       new_task = Todo(content=task_content)
       if  not task_content:
           return 'Please enter valid task!'
       try:
           db.session.add(new_task)
           db.session.commit()
           return redirect("/")
       except:
           return 'Error in adding task to database'
    else:
        #get request
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

#Delete route
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "Problem deteling the seleted task"

#Modify route
@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    
    if request.method=='POST':
        task.content = request.form["task"]

        try:
           db.session.commit()
           return redirect("/")
        except:
              return 'Error in modifying task'
    else:
        return render_template('modify.html', task=task)


if __name__ == '__main__':
    app.run()
