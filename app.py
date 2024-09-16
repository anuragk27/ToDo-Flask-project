from flask import Flask , render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy  
from datetime import datetime

 
app = Flask(__name__) #creating the Flask class object   
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/',methods=['GET','POST'] ) #decorator drfines the   
def home():
    if request.method == 'POST':
        title = request.form['title'] #get from form
        print(title)
        todo = Todo(title=title) 
        db.session.add(todo) #add to db
        db.session.commit()
    allTodo = Todo.query.all() #fetch from db
    print(allTodo)
    return render_template("index.html",allTodo=allTodo)


@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):  
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        todo.title = request.form['title']
        db.session.commit()
        return redirect('/')
    return render_template('update.html',todo=todo)


@app.route('/delete/<int:sno>')
def delete(sno):  
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ =='__main__':  
    app.run(debug = True)  