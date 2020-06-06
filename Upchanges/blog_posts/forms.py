from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class BlogPostForm(FlaskForm):
    blog_image = FileField('Add picture of the problem+ / Update picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    #In the future, I may need to create a WebP image conversion, converting all image from the users to webp in the back end, reducing the size of all images'size: https://qiita.com/hengsokvisal/items/e4610ec5c39a2f0045cc
    problem_name = StringField('Problem Name', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    problem_type = SelectField('Type of Problem', choices=[('education','Education'),('health','Health'),('environment','Environment'),('economics','Economics'),('society','Society')],validators=[DataRequired()])
    country = SelectField('Country location', choices=[('Vietnam', 'Vietnam'), ('Japan', 'Japan'),('United States of America', 'United States of America')], validators=[DataRequired()])
    problem_submit = SubmitField("Post")