from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


app.config['DEBUG'] = True
#setup connection to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:vera2012@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app) #create object constructor
app.secret_key = 'ghyuhaskh234445'

#using class called db.model so all objects inherit from this class
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)#id is an instance of this column
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   

    def __init__(self, title, body, owner): #this is a constructor that initializes
        self.title = title
        self.body = body
        self.owner= owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request 
def require_login():
    allowed_routes = ['login','signup','blogPage','index'] #list of routes users dont need to be logged ion to see
    if request.endpoint not in allowed_routes and 'username' not in session: 
        return redirect('/login') 

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first() 
        if user and user.password == password:
            session['username'] = username # - "remember" that the user has logged in
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error') # 'error' is a category we use a placeholder on base.html to make it a class to turn text red
            return render_template('login.html')

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        #TODO - validate

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            if (not username) or (username.strip() == '') or (not password) or (password.strip() == '') or (not verify) or (verify.strip() == ''):
                flash('Please complete the form by filling all boxes', 'error')
                return render_template('signup.html', username=username)
            if len(username)<3 or len(username)>20 or (not username) or (username.strip() == ''):
                flash('Please enter valid username', 'error')
                return render_template('signup.html', username=username)
            if len(password)<3 or len(password)>20 or (not password) or (password.strip() == ''):
                flash('Please enter valid password', 'error')
                return render_template('signup.html', username=username)
            if verify != password:
                flash('Passwords do not match', 'error')
                return render_template('signup.html', username=username)
            

            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username # - "remember" that the user has logged in
            return redirect('/newpost')

        else:
            #TODO - user better response messaging
            flash('Sorry that username is taken', 'error')
            return render_template('signup.html')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username'] #<---removes the email session to stop "remembering" user is logged in.
    return redirect('/blog')

@app.route('/blog', methods=['POST','GET'])  
def blogPage():
    id = request.args.get('id') #this grabs the id from the query parameter in the URL after the ? --> /blog?id=
    user = request.args.get('user')
    if id == id:    
        
        if id == None: #if there is no id then it renders the main blog page
            btitle = Blog.query.all()
            return render_template('blog.html', btitle=btitle)
   
        else:
            get_blog = Blog.query.get(id) #this creates a query object called get_blog to use to talk to database
            blogtitle = get_blog.title
            blogpost = get_blog.body
            return render_template('singleblog.html',blogtitle=blogtitle,blogpost=blogpost)
    if user == user:
            get_userBlog = Blog.query.get(owner_id)
            blogtitle= get_userBlog.title
            blogpost = get_userBlog.body
            return render_template('singleUser.html',blogtitle=blogtitle,blogpost=blogpost)
    else:
        return redirect('/')

        
        
       


 
  
@app.route('/newpost', methods=['POST','GET'])
def newpost():
    titleError=""
    bodyError=""
    
    if request.method == 'POST':
        # set variables to retrieve and store user input for title and body
        blogtitle = request.form['blogtitle']  
        blogpost = request.form['blogpost']
        owner = User.query.filter_by(username=session['username']).first()
        new_title = Blog(blogtitle,blogpost,owner)  #makes new object for title and body 

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

        else:
            return render_template('newpost.html',blogtitle=blogtitle, blogpost=blogpost, titleError=titleError, bodyError=bodyError)

    return render_template('newpost.html')
    

@app.route('/', methods=['POST','GET'])
def index():
    id = request.args.get('id')
    if id == None:
        userList = User.query.all()
        return render_template('index.html', userList=userList)
    else:
       
        return redirect('/')
         

  
 


if __name__ == '__main__': #if you want to reference this from somewhere else this lets you import 
    app.run()


        




