from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from Upchanges import db
from Upchanges.models import BlogPost, BlogInfo
from Upchanges.blog_posts.forms import BlogPostForm
from Upchanges.blog_info.forms import BlogInfoForm
from Upchanges.users.picture_handler import add_blog_pic


blog_posts = Blueprint('blog_posts',__name__)

#Create
@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():

        blog_validated = BlogPost(problem_name=form.problem_name.data,
                                  text=form.text.data,
                                  user_id=current_user.id,
                                  blog_image=add_blog_pic(form.blog_image.data, form.problem_name.data+str(current_user.id)),
                                  problem_type=form.problem_type.data,
                                  country=form.country.data)


        blog_image = url_for('static', filename='profile_pics/' + blog_validated.blog_image)
        db.session.add(blog_validated)
        db.session.commit()
        flash('Blog Post Created')
        return redirect(url_for('core.index', blog_image=url_for('static', filename='profile_pics/' + blog_validated.blog_image)))

    return render_template('create_post.html', form=form)




#View blog post
@blog_posts.route('/<int:blog_validated_id>', methods=['GET', 'POST']) #int makes a string a number so that BlogPost.query doesn't show error(because data can only stored as number)
def blog_view(blog_validated_id):
    blog_view = BlogPost.query.get_or_404(blog_validated_id)#check to see if a blog with an id exist, if not, return 404



    form2=BlogInfoForm()

    if form2.validate_on_submit():

        blog_comment_validated = BlogInfo(text=form2.text.data,
                                          user_id=current_user.id,
                                          blog_post_id=blog_validated_id)
        db.session.add(blog_comment_validated)
        db.session.commit()
        flash("Blog's comment added")

        page = request.args.get('page', 1, type=int)
        comment_blogs1 = BlogInfo.query.filter(BlogInfo.blog_post_id.ilike(blog_validated_id)).order_by(BlogInfo.date.desc())
        comment_blogs = comment_blogs1.paginate(page=page,per_page=2)
        comment_blogs_num = comment_blogs1.count()

        return redirect(url_for('blog_posts.blog_view', problem_name=blog_view.problem_name,
                           date=blog_view.date,
                           blog_image=blog_view.blog_image,
                           post=blog_view,
                           problem_type= blog_view.problem_type, form2=form2,comment_blogs=comment_blogs, comment_text=blog_comment_validated.text, blog_validated_id=blog_validated_id, page=page,
                                comment_blogs_num=comment_blogs_num))


    page = request.args.get('page', 1, type=int)
    comment_blogs1 = BlogInfo.query.filter(BlogInfo.blog_post_id.ilike(blog_validated_id)).order_by(BlogInfo.date.desc())
    comment_blogs = comment_blogs1.paginate(page=page, per_page=2)
    comment_blogs_num = comment_blogs1.count()
    return render_template('blog_view.html', problem_name=blog_view.problem_name,
                           date=blog_view.date,
                           blog_image=blog_view.blog_image,
                           post=blog_view,
                           problem_type= blog_view.problem_type, form2=form2, comment_blogs=comment_blogs, blog_validated_id=blog_validated_id, page=page,
                           comment_blogs_num=comment_blogs_num)

# put post_next=blog_next after post=blog_view, later(trying to create a blog_id+1's id for the alignment of blogs)


#Update
@blog_posts.route('/<int:blog_validated_id>/update', methods=['GET', 'POST'])
@login_required
def update(blog_validated_id):
    blog_update = BlogPost.query.get_or_404(blog_validated_id)

    if blog_update.creator != current_user: #if creator of the blog is not the current user
        abort(403)  #show 403 no permission page

    form = BlogPostForm()  #Creating an instance by writing A= B() ;creating an instance of B using A


    if form.validate_on_submit():

        if form.blog_image.data:
            blog_update.blog_image = add_blog_pic(form.blog_image.data, form.problem_name.data + str(current_user.id))
            # blog_update.blog_image=blog_image

        blog_update.problem_name = form.problem_name.data
        blog_update.text = form.text.data
        blog_update.problem_type = form.problem_type.data
        blog_update.country = form.country.data
        db.session.commit()
        flash('Blog Post Updated')
        return redirect(url_for('blog_posts.blog_view',blog_validated_id=blog_update.blog_id, blog_image=url_for('static', filename='blog_pics/' + blog_update.blog_image)))

    elif request.method =='GET':
        form.problem_name.data = blog_update.problem_name
        form.text.data = blog_update.text
        form.blog_image.data=blog_update.blog_image
        form.problem_type.data=blog_update.problem_type
        form.country.data=blog_update.country



    return render_template('create_post.html', form=form)




#Delete
@blog_posts.route('/<int:blog_validated_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(blog_validated_id):

    blog_delete = BlogPost.query.get_or_404(blog_validated_id)
    comment_blogs1 = BlogInfo.query.filter(BlogInfo.blog_post_id.ilike(blog_validated_id))
    comment_blogs_num = comment_blogs1.count()


    if blog_delete.creator != current_user: #if creator of the blog is not the current user
        abort(403)  #show 403 no permission page
    if comment_blogs_num >= 2:
        abort(403)

    db.session.delete(blog_delete)
    db.session.commit()
    flash('Blog Post Deleted')
    return redirect(url_for('core.index'))





@blog_posts.route('/<int:blog_validated_id>/<int:blog_info_id>/update', methods=['GET', 'POST'])
@login_required
def blog_info_update(blog_validated_id, blog_info_id):

    blog_view = BlogPost.query.get_or_404(blog_validated_id)
    blog_info_update = BlogInfo.query.get_or_404(blog_info_id)

    page = request.args.get('page', 1, type=int)
    comment_blogs1 = BlogInfo.query.filter(BlogInfo.blog_post_id.ilike(blog_validated_id)).order_by(BlogInfo.date.desc())
    comment_blogs = comment_blogs1.paginate(page=page, per_page=2)
    comment_blogs_num = comment_blogs1.count()

    if blog_info_update.comment!= current_user:
        abort(403)

    form2 = BlogInfoForm()

    if form2.validate_on_submit():
        blog_info_update.text=form2.text.data
        db.session.commit()
        flash('Blog info post is updated')
        return redirect(url_for('blog_posts.blog_view', blog_validated_id=blog_validated_id, form2=form2, comment_blogs=comment_blogs, page=page,
                           comment_blogs_num=comment_blogs_num,
                                blog_info_id=blog_info_update.blog_info_id,
                                problem_name=blog_view.problem_name,
                                date=blog_view.date,
                                blog_image=blog_view.blog_image,
                                post=blog_view,
                                problem_type=blog_view.problem_type))

    elif request.method == 'GET':
        form2.text.data = blog_info_update.text

    return render_template('blog_view.html', blog_validated_id=blog_validated_id, form2=form2, comment_blogs=comment_blogs, page=page,
                           comment_blogs_num=comment_blogs_num,
                                blog_info_id=blog_info_update.blog_info_id,
                                problem_name=blog_view.problem_name,
                                date=blog_view.date,
                                blog_image=blog_view.blog_image,
                                post=blog_view,
                                problem_type=blog_view.problem_type)


@blog_posts.route('/<int:blog_validated_id>/<int:blog_info_id>/delete', methods=['GET', 'POST'])
@login_required
def blog_info_delete(blog_info_id,blog_validated_id):

    blog_info_delete = BlogInfo.query.get_or_404(blog_info_id)
    comment_blogs1 = BlogInfo.query.filter(BlogInfo.blog_post_id.ilike(blog_validated_id))
    comment_blogs_num = comment_blogs1.count()


    if blog_info_delete.comment != current_user:
        abort(403)

    if comment_blogs_num >= 2:
        abort(403)

    db.session.delete(blog_info_delete)
    db.session.commit()
    flash('Blog info comment is deleted')
    return redirect(url_for('blog_posts.blog_view', blog_validated_id=blog_validated_id))

