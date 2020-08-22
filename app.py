from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# set up the app, referencing this file
app = Flask(__name__)

## DATABASE
    # test.db is where teh database going to be, everything is going to be store in test.db file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'     # ///:relative , ////:absolute_path
    # Initialize our database 
db = SQLAlchemy(app)

    # Create a model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    complete = db.Column(db.Integer,default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self):
        return "<Task %r>" %self.id
    
# create an index route
@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)


if __name__ == "__main__":
    app.run(debug=True)     # if there's an error happened, it will pop up on the web

