from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length

class InsertForm(Form):
    sample_id = StringField('sample_id', validators=[DataRequired(),
                            Length(min=1, max=8)])
    name = StringField('name', validators=[Length(min=0, max=20)])
    generation = StringField('generation', validators=[Length(min=0, max=9)])
    sex = RadioField('sex', default='',
                     choices=[('1', 'Male'), ('2', 'Female'), 
                              ('', 'Unkown')])
    mother = StringField('mother', validators=[Length(min=0, max=8)])
    father = StringField('father', validators=[Length(min=0, max=8)])
    notes = TextAreaField('notes', validators=[Length(min=0, max=255)])

class UpdateForm(InsertForm):
    new_sample_id = StringField('new_sample_id', 
                                validators=[Length(min=0, max=8)])

class DeleteForm(Form):
    sample_id = StringField('sample_id', validators=[DataRequired()])
