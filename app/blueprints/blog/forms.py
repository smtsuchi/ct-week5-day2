from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    image = StringField('Image')
    content = TextAreaField('Content Here', validators=[DataRequired()])
    submit = SubmitField()
