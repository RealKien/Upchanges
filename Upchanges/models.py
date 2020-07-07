from Upchanges import db, LoginManager, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

##ACITVATE LOGIN MANAGER#####
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    #The function above make "if user is authenticated" sort of stuff possible




class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(64), nullable=False, default='default_profile.jpg' ) #nullable means "it cannot be blank"
    email = db.Column(db.String(64), unique=True, index=True) #DON'T REALLY GET THE IDEA OF index=True
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    middle_name = db.Column(db.String(20), default='', nullable=True)
    username = first_name+middle_name+last_name
    password_hash = db.Column(db.String(128))


    posts = db.relationship('BlogPost', backref='creator', lazy=True)#db.relationship is to connect different database together
    bloginfos = db.relationship('BlogInfo', backref= 'comment', lazy=True)
    blogideas = db.relationship('BlogIdea', backref='idea_creator', lazy=True)

    def __init__(self,email,first_name, middle_name, last_name, password):     #This is so that we can use the database for other files in this folder Upchanges.
        self.email = email
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Username: {self.username}"



class BlogPost(db.Model):
    __tablename__ = 'blog_post'
    users = db.relationship(User)

    blog_id = db.Column(db.Integer, primary_key=True)
    # blog_next = db.Column(blog_id()+1)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False) #users.id  is taken from the tablename(users) and id in its table
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  #Automatically post the time of the post
    problem_name = db.Column(db.String(140), nullable=False)
    text = db.Column(db.Text, nullable=False)
    blog_image = db.Column(db.String(140), nullable=False, server_default='default_blog.jpg')
    problem_type = db.Column(db.String(140), nullable=False, server_default='test_type')
    country = db.Column(db.String(140), nullable=False, server_default='Earth')
    ###IF I CAN'T FIX THE BLOG_IMAGE ERRORS, I CAN JUST COMMENT OFF THOSE CODES THAT RELATE TO THEM###
    bloginfos2 = db.relationship('BlogInfo', backref="comment2", lazy=True)
    blogideas2 = db.relationship('BlogInfo', backref="idea_creator2", lazy=True)

    def __init__(self, text, problem_name, user_id, blog_image, problem_type, country):
        self.text = text
        self.problem_name = problem_name
        self.user_id = user_id
        self.blog_image = blog_image
        self.problem_type = problem_type
        self.country = country

        #When I put a new column in the init, it will require the user to input something in the create blog



    def __repr__(self):
        return f"Post ID: {self.blog_id} -- Date:{self.date}---{self.problem_name}"



class BlogInfo(db.Model):
    __tablename__ = 'blog_info'

    users=db.relationship(User)
    blog_post=db.relationship(BlogPost)

    blog_info_id = db.Column(db.Integer, primary_key=True)
    blog_post_id = db.Column(db.Integer, db.ForeignKey('blog_post.blog_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, blog_post_id, user_id, text):
        self.blog_post_id = blog_post_id
        self.user_id = user_id
        self.text = text

    def __repr__(self):
        return f"Blog's comment ID:{self.blog_info_id} -- Date:{self.date} -- {self.text}"




class BlogIdea(db.Model):
    __tablename__ = 'blog_idea'

    users = db.relationship(User)
    blog_post = db.relationship(BlogPost)

    blog_idea_id = db.Column(db.Integer, primary_key=True)
    blog_post_id = db.Column(db.Integer, db.ForeignKey('blog_post.blog_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, blog_post_id, user_id, text):
        self.blog_post_id = blog_post_id
        self.user_id = user_id
        self.text = text

    def __repr__(self):
        return f"Blog idea ID: {self.blog_idea_id} -- Date: {self.date} -- {self.text}"

