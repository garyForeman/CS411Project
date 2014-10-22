from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, RadioField, IntegerField
from wtforms import BooleanField
from wtforms.validators import DataRequired, Length, Optional
from app.SQLfunctions import SAMPLE_TABLE, GENOTYPE_TABLE, MARKER_TABLE
from app.SQLfunctions import ATTRIBUTES

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

class InsertGenotypeForm(Form):
    sample_id = StringField('sample_id',
                            validators=[DataRequired(), Length(min=1, max=8)])
    marker_id = StringField('marker_id',
                            validators=[DataRequired(), Length(min=1, max=15)])
    genotype1 = IntegerField('genotype1', validators=[Optional()])
    genotype2 = IntegerField('genotype2', validators=[Optional()])

class UpdateSampleForm(InsertSampleForm):
    new_sample_id = StringField('new_sample_id',
                                validators=[Length(min=0, max=8)])

class UpdateMarkerForm(InsertMarkerForm):
    new_marker_id = StringField('new_marker_id',
                                validators=[Length(min=0, max=15)])

class UpdateGenotypeForm(InsertGenotypeForm):
    new_sample_id = StringField('new_sample_id',
                                validators=[Length(min=0, max=8)])
    new_marker_id = StringField('new_marker_id',
                                validators=[Length(min=0, max=15)])

class DeleteSampleForm(Form):
    sample_id = StringField('sample_id', validators=[DataRequired()])

class DeleteMarkerForm(Form):
    marker_id = StringField('marker_id', validators=[DataRequired()])

class DeleteGenotypeForm(Form):
    sample_id = StringField('sample_id', validators=[DataRequired()])
    marker_id = StringField('marker_id', validators=[DataRequired()])

class QueryForm(Form):
    sample_all = BooleanField('All Sample Table Columns', default=False)
    sample_sample_id = BooleanField('Sample ID (' + SAMPLE_TABLE + '.' +
                                    ATTRIBUTES[SAMPLE_TABLE][0] + ')',
                                    default=False)
    sample_name = BooleanField('Name (' + SAMPLE_TABLE + '.' +
                               ATTRIBUTES[SAMPLE_TABLE][1] + ')',
                               default=False)
    sample_generation = BooleanField('Generation (' + SAMPLE_TABLE + '.' +
                                     ATTRIBUTES[SAMPLE_TABLE][2] + ')',
                                     default=False)
    sample_sex = BooleanField('Sex (' + SAMPLE_TABLE + '.' +
                              ATTRIBUTES[SAMPLE_TABLE][3] + ')',
                              default=False)
    sample_mother = BooleanField('Mother (' + SAMPLE_TABLE + '.' +
                                 ATTRIBUTES[SAMPLE_TABLE][4] + ')',
                                 default=False)
    sample_father = BooleanField('Father (' + SAMPLE_TABLE + '.' +
                                 ATTRIBUTES[SAMPLE_TABLE][5] + ')',
                                 default=False)
    sample_notes = BooleanField('Notes (' + SAMPLE_TABLE + '.' +
                                ATTRIBUTES[SAMPLE_TABLE][6] + ')',
                                default=False)

    genotype_all = BooleanField('All Genotype Table Columns', default=False)
    genotype_sample_id = BooleanField('Sample ID (' + GENOTYPE_TABLE + '.' +
                                      ATTRIBUTES[GENOTYPE_TABLE][0] + ')',
                                      default=False)
    genotype_marker_id = BooleanField('Marker ID (' + GENOTYPE_TABLE + '.' +
                                      ATTRIBUTES[GENOTYPE_TABLE][1] + ')',
                                      default=False)
    genotype_genotype1 = BooleanField('Genotype Pair Member 1 (' +
                                      GENOTYPE_TABLE + '.' +
                                      ATTRIBUTES[GENOTYPE_TABLE][2] + ')',
                                      default=False)
    genotype_genotype2 = BooleanField('Genotype Pair Member 2 (' +
                                      GENOTYPE_TABLE + '.' +
                                      ATTRIBUTES[GENOTYPE_TABLE][3] + ')',
                                      default=False)

    marker_all = BooleanField('All Marker Table Columns', default=False)
    marker_marker_id = BooleanField('Marker ID (' + MARKER_TABLE + '.' +
                                    ATTRIBUTES[MARKER_TABLE][0] + ')',
                                    default=False)
    marker_meiotic_pos = BooleanField('Meiotic Position (' + MARKER_TABLE +
                                      '.' + ATTRIBUTES[MARKER_TABLE][1] + ')',
                                      default=False)
    marker_dog_chrom = BooleanField('Dog Chromose (' + MARKER_TABLE + '.' +
                                    ATTRIBUTES[MARKER_TABLE][2] + ')',
                                    default=False)
    marker_dog_pos = BooleanField('Dog Position (' + MARKER_TABLE + '.' +
                                  ATTRIBUTES[MARKER_TABLE][3] + ')',
                                  default=False)
    marker_fox_seq = BooleanField('Fox Sequence (' + MARKER_TABLE + '.' +
                                  ATTRIBUTES[MARKER_TABLE][4] + ')',
                                  default=False)
    marker_fox_chrom = BooleanField('Fox Chromosome (' + MARKER_TABLE + '.' +
                                    ATTRIBUTES[MARKER_TABLE][5] + ')',
                                    default=False)
    marker_fox_pos = BooleanField('Fox Position (' + MARKER_TABLE + '.' +
                                  ATTRIBUTES[MARKER_TABLE][6] + ')',
                                  default=False)

    where_clause = TextAreaField('where_clause')
