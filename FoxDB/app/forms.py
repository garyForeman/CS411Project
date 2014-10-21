from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, RadioField, IntegerField
from wtforms.validators import DataRequired, Length, Optional

class InsertSampleForm(Form):
    sample_id = StringField('sample_id',
                            validators=[DataRequired(), Length(min=1, max=8)])
    name = StringField('name', validators=[Length(min=0, max=20)])
    generation = StringField('generation', validators=[Length(min=0, max=9)])
    sex = RadioField('sex', default='',
                     choices=[('1', 'Male'), ('2', 'Female'),
                              ('', 'Unkown')])
    mother = StringField('mother', validators=[Length(min=0, max=8)])
    father = StringField('father', validators=[Length(min=0, max=8)])
    notes = TextAreaField('notes', validators=[Length(min=0, max=255)])

class InsertMarkerForm(Form):
    marker_id = StringField('marker_id',
                            validators=[DataRequired(), Length(min=1, max=15)])
    meiotic_pos = StringField('meiotic_pos', validators=[Length(min=0, max=5)])
    dog_chrom = StringField('dog_chrom', validators=[Length(min=0, max=2)])
    dog_pos = IntegerField('dog_pos', validators=[Optional()])
    fox_seg = StringField('fox_seg',
                          validators=[Length(min=0, max=15)])
    fox_chrom = StringField('fox_chrom', validators=[Length(min=0, max=15)])
    fox_pos = IntegerField('fox_pos', validators=[Optional()])

class UpdateSampleForm(InsertSampleForm):
    new_sample_id = StringField('new_sample_id',
                                validators=[Length(min=0, max=8)])

class UpdateMarkerForm(InsertMarkerForm):
    new_marker_id = StringField('new_marker_id',
                                validators=[Length(min=0, max=15)])

class DeleteSampleForm(Form):
    sample_id = StringField('sample_id', validators=[DataRequired()])

class DeleteMarkerForm(Form):
    marker_id = StringField('marker_id',
                            validators=[Length(min=0, max=15)])
