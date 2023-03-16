from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length, InputRequired

class SearchForm(FlaskForm):
    search_query = StringField('query', validators=[InputRequired(), Length(min=1, max=30, message='Must be at least 1 character long and no more than 30 characteres')])
    
    submit = SubmitField('btn btn-outline-success')


class MovieReviewForm(FlaskForm):
    name = StringField('Name or Alias', validators=[InputRequired(), Length(min=1, max=50)])

    text = TextAreaField('Comment', validators=[Length(min=1, max=500)])

    submit = SubmitField()