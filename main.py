from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:vera2012@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)




class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
   

    def __init__(self, title, body):
        self.title = title
        self.body= body



@app.route('/', methods=['POST','GET'])
def index():
    
    if request.method == 'POST':
        blogtitle = request.form['title']   
        new_title = Blog(blogtitle)        
        blogpost = request.form['body']
        blog_Post = Blog(blogpost)
        db.session.add(new_title,blog_Post)
    
    title = Blog.query.all()
    body = Blog.query.all()

    return render_template('index.html', title=title, body=body)





if __name__ == '__main__':
    app.run()


        




