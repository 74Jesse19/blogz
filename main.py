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
    id = request.args.get('id')
    if id == None:
        btitle = Blog.query.all()
        return render_template('blog.html', btitle=btitle)
    else: 
        #blog_id = int(request.form['word-id'])

        blogtitle = Blog.query.get('word-title')
        blogpost = request.args.get('word.body')
        return render_template('singleblog.html',blogtitle=blogtitle,blogpost=blogpost)

 
  
@app.route('/newpost', methods=['POST','GET'])
def newpost():
    titleError=""
    bodyError=""
    
    if request.method == 'POST':
        # set variables to retrieve and store user input for title and body
        blogtitle = request.form['blogtitle']  
        blogpost = request.form['blogpost']
        new_title = Blog(blogtitle,blogpost)  #makes new object for title and body 

        #data validation 
        if not blogtitle:
            titleError = "Please fill in the title"
        
        if not blogpost:
            bodyError = "Please fill in the body" 

        if not titleError and not bodyError:
            
            
        
            db.session.add(new_title) #adds to database
            db.session.commit()# dont forget this you need it to commit add
            id = str(new_title.id)
            return redirect('/blog?id={0}'.format(id))

            #else:  ** this works but only in the newpost handler **
                #blogtitle = request.args.get(new_title.id, new_title.title)
                #blogpost = request.args.get(new_title.id, new_title.body)
                #return render_template('/singleblog.html',blogtitle=blogtitle, blogpost=blogpost)

        else:
            return render_template('newpost.html',blogtitle=blogtitle, blogpost=blogpost, titleError=titleError, bodyError=bodyError)

    return render_template('newpost.html')
    

@app.route('/', methods=['POST','GET'])
def index():

    return render_template('newpost.html')
 


if __name__ == '__main__': #if you want to reference this from somewhere else this lets you import 
    app.run()


        




