#create the view function for some main pages
import os

from flask import render_template, request, Blueprint, url_for, flash, redirect
from sqlalchemy import or_, null

from Upchanges.core.forms import Blogsearch_form
from Upchanges.models import BlogPost
import _sqlite3



import os
print("MY FILE = ", os.path.realpath(__file__))
MYDIR = os.path.dirname(__file__)
print("MYDIR = ", os.path.realpath(MYDIR))
SQLPATH = os.path.join(MYDIR, "..", "data.sqlite")
print("This gives me SQLPATH = ", os.path.realpath(SQLPATH))
conn = _sqlite3.connect(SQLPATH, check_same_thread=False)  #This path is righ! How can still it is not working>
c = conn.cursor()




core = Blueprint('core', __name__)

#MAIN PAGE
@core.route('/', methods=['GET', 'POST'])
def index():
    # Call a function to later use in creating the template
    form = Blogsearch_form(request.form)


    if request.method == 'POST':
        id_list = [i[0] for i in BlogPost.query.with_entities(BlogPost.blog_id).filter(BlogPost.problem_name.ilike("%" + form.search.data  + "%")).all()] #This code on the left side doesn't do anything, it's just there to help me to learn to code

        page = request.args.get('page', 1, type=int)

        many_posts0 = BlogPost.query.filter(or_((BlogPost.problem_name.ilike("%" + form.search.data + "%")),(BlogPost.text.ilike("%" + form.search.data + "%")))).order_by(BlogPost.date.desc())
        many_posts = many_posts0.paginate(page=page, per_page=10)
        num_posts = many_posts0.count()
        if num_posts == 0:
            no_posts="Couldn't find relating problems"
        else:
            no_posts=''

        return render_template('blog_search_result.html', id_list=id_list, many_posts=many_posts, num_posts=num_posts, no_posts=no_posts)



    page = request.args.get('page',1,type=int)
    many_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=10)
    return render_template('index.html', many_posts=many_posts, form=form)


@core.route('/education', methods=['GET', 'POST'])
def education():

    form = Blogsearch_form(request.form)
    page = request.args.get('page', 1, type=int)
    many_posts = BlogPost.query.filter(BlogPost.problem_type.ilike('education')).order_by(BlogPost.date.desc()).paginate(page=page, per_page=10)

    if request.method == 'POST':
        id_list = [i[0] for i in BlogPost.query.with_entities(BlogPost.blog_id ).filter(BlogPost.problem_name.ilike("%" + form.search.data  + "%")).all()] #This code on the left side doesn't do anything, it's just there to help me to learn to code

        page = request.args.get('page', 1, type=int)

        many_posts0 = BlogPost.query.filter(or_((BlogPost.problem_name.ilike("%" + form.search.data + "%")),(BlogPost.text.ilike("%" + form.search.data + "%")))).order_by(BlogPost.date.desc())
        many_posts = many_posts0.paginate(page=page, per_page=10)
        num_posts = many_posts0.count()
        if num_posts == 0:
            no_posts="Couldn't find relating problems"
        else:
            no_posts=''

        return render_template('blog_search_result.html', id_list=id_list, many_posts=many_posts, num_posts=num_posts,
                           no_posts=no_posts)


    return render_template('index1.html', many_posts=many_posts, form=form)

@core.route('/health', methods=['GET', 'POST'])
def health():
    form = Blogsearch_form(request.form)
    page = request.args.get('page', 1, type=int)
    many_posts = BlogPost.query.filter(BlogPost.problem_type.ilike('health')).order_by(BlogPost.date.desc()).paginate(page=page, per_page=10)

    if request.method == 'POST':
        id_list = [i[0] for i in BlogPost.query.with_entities(BlogPost.blog_id ).filter(BlogPost.problem_name.ilike("%" + form.search.data  + "%")).all()] #This code on the left side doesn't do anything, it's just there to help me to learn to code

        page = request.args.get('page', 1, type=int)

        many_posts0 = BlogPost.query.filter(or_((BlogPost.problem_name.ilike("%" + form.search.data + "%")),(BlogPost.text.ilike("%" + form.search.data + "%")))).order_by(BlogPost.date.desc())
        many_posts = many_posts0.paginate(page=page, per_page=10)
        num_posts = many_posts0.count()
        if num_posts == 0:
            no_posts="Couldn't find relating problems"
        else:
            no_posts=''

        return render_template('blog_search_result.html', id_list=id_list, many_posts=many_posts, num_posts=num_posts,
                           no_posts=no_posts)


    return render_template('index1.html', many_posts=many_posts, form=form)

@core.route('/environment', methods=['GET', 'POST'])
def environment():
    form = Blogsearch_form(request.form)
    page = request.args.get('page', 1, type=int)
    many_posts = BlogPost.query.filter(BlogPost.problem_type.ilike('environment')).order_by(BlogPost.date.desc()).paginate(page=page, per_page=10)

    if request.method == 'POST':
        id_list = [i[0] for i in BlogPost.query.with_entities(BlogPost.blog_id ).filter(BlogPost.problem_name.ilike("%" + form.search.data  + "%")).all()] #This code on the left side doesn't do anything, it's just there to help me to learn to code

        page = request.args.get('page', 1, type=int)

        many_posts0 = BlogPost.query.filter(or_((BlogPost.problem_name.ilike("%" + form.search.data + "%")),(BlogPost.text.ilike("%" + form.search.data + "%")))).order_by(BlogPost.date.desc())
        many_posts = many_posts0.paginate(page=page, per_page=10)
        num_posts = many_posts0.count()
        if num_posts == 0:
            no_posts="Couldn't find relating problems"
        else:
            no_posts=''

        return render_template('blog_search_result.html', id_list=id_list, many_posts=many_posts, num_posts=num_posts,
                           no_posts=no_posts)

    return render_template('index1.html', many_posts=many_posts, form=form)

@core.route('/economics', methods=['GET', 'POST'])
def economics():
    form = Blogsearch_form(request.form)
    page = request.args.get('page', 1, type=int)
    many_posts = BlogPost.query.filter(BlogPost.problem_type.ilike('economics')).order_by(BlogPost.date.desc()).paginate(page=page, per_page=10)

    if request.method == 'POST':
        id_list = [i[0] for i in BlogPost.query.with_entities(BlogPost.blog_id ).filter(BlogPost.problem_name.ilike("%" + form.search.data  + "%")).all()] #This code on the left side doesn't do anything, it's just there to help me to learn to code

        page = request.args.get('page', 1, type=int)

        many_posts0 = BlogPost.query.filter(or_((BlogPost.problem_name.ilike("%" + form.search.data + "%")),(BlogPost.text.ilike("%" + form.search.data + "%")))).order_by(BlogPost.date.desc())
        many_posts = many_posts0.paginate(page=page, per_page=10)
        num_posts = many_posts0.count()
        if num_posts == 0:
            no_posts="Couldn't find relating problems"
        else:
            no_posts=''

        return render_template('blog_search_result.html', id_list=id_list, many_posts=many_posts, num_posts=num_posts,
                           no_posts=no_posts)

    return render_template('index1.html', many_posts=many_posts, form=form)

@core.route('/society', methods=['GET', 'POST'])
def society():
    form = Blogsearch_form(request.form)
    page = request.args.get('page', 1, type=int)
    many_posts = BlogPost.query.filter(BlogPost.problem_type.ilike('society')).order_by(BlogPost.date.desc()).paginate(page=page, per_page=10)

    if request.method == 'POST':
        id_list = [i[0] for i in BlogPost.query.with_entities(BlogPost.blog_id ).filter(BlogPost.problem_name.ilike("%" + form.search.data  + "%")).all()] #This code on the left side doesn't do anything, it's just there to help me to learn to code

        page = request.args.get('page', 1, type=int)

        many_posts0 = BlogPost.query.filter(or_((BlogPost.problem_name.ilike("%" + form.search.data + "%")),(BlogPost.text.ilike("%" + form.search.data + "%")))).order_by(BlogPost.date.desc())
        many_posts = many_posts0.paginate(page=page, per_page=10)
        num_posts = many_posts0.count()
        if num_posts == 0:
            no_posts="Couldn't find relating problems"
        else:
            no_posts=''

        return render_template('blog_search_result.html', id_list=id_list, many_posts=many_posts, num_posts=num_posts,
                           no_posts=no_posts)

    return render_template('index1.html', many_posts=many_posts, form=form)

@core.route('/info')
def info():
    return render_template('info.html')