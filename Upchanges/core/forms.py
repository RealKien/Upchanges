from wtforms import Form, StringField, SelectField
from flask import render_template
from Upchanges.models import BlogPost


class Blogsearch_form(Form):
    search = StringField('')      #THIS MODEL BLOG SEARCH IS NOT STORING ANY DATA.

#This Blogsearch_form should be the other model Blog_Post