from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class UpdateForm(Form):
    sample_id = StringField('sample_id', validators=[DataRequired()]) 
