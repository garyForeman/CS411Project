from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class InsertForm(Form):
    sample_id = StringField('sample_id', validators=[DataRequired()])
    #name = StringField('name')
    #generation = StringField('generation')
    #sex = 

class DeleteForm(Form):
    sample_id = StringField('sample_id', validators=[DataRequired()])
