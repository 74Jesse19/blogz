from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


app.config['DEBUG'] = True
#setup connection to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:vera2012@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app) #create object constructor

#using class called db.model so all objects inherit from this class
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)#id is an instance of this column
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
   

    def __init__(self, title, body): #this is a constructor that initializes
        self.title = title
        self.body= body

@app.route('/blog', methods=['POST','GET'])  
def blogPage():
    btitle = Blog.query.all()
    body = Blog.query.all()
    return render_template('blog.html',title= " ADD BLOG ENTRY", btitle=btitle, body=body)
  



@app.route('/newpost', methods=['POST','GET'])
def newpost():
    titleError=""
    bodyError=""
    print("******in function")
    if request.method == 'POST':
        # set variables to retrieve and store user input for title and body
        blogtitle = request.form['blogtitle']   
        blogpost = request.form['blogpost']
        new_title = Blog(blogtitle,blogpost)  #makes new object for title and body 
        #data validation
        if not blogtitle:
            titleError = "Please fill in the title"
        
        if not blogpost:
            bodyError = "Please fill in the body" # look at this part it is whats broke

        if not titleError and not bodyError:
            
            db.session.add(new_title) #adds to database
            db.session.commit()# dont forget this you need it to commit add
            id= str(new_title.id)
            btitle = Blog.query.all()
            body = Blog.query.all()
            return redirect('/blog')
        
        

        else:
            print('*********errors here', titleError, bodyError)
            return render_template('newpost.html',blogtitle=blogtitle, blogpost=blogpost, titleError=titleError, bodyError=bodyError)

    return render_template('newpost.html')

 
@app.route('/', methods=['POST','GET'])
def index():

    return render_template('newpost.html')
 


if __name__ == '__main__': #if you want to reference this from somewhere else this lets you import 
    app.run()


        




