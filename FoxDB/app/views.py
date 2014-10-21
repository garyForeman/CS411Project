from flask import render_template, flash, redirect
from app import app
from .forms import InsertSampleForm, UpdateSampleForm, DeleteSampleForm
from .forms import InsertMarkerForm, UpdateMarkerForm, DeleteMarkerForm
from flask import g
from app.SQLfunctions import DB_NAME, DB_HOST, DB_USER, DB_PASSWD
from app.SQLfunctions import db_insert, db_update, db_delete
from app.SQLfunctions import SAMPLE_TABLE, MARKER_TABLE
import MySQLdb

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    sample_form = InsertSampleForm(prefix='sample_form')
    marker_form = InsertMarkerForm(prefix='marker_form')
    if sample_form.validate_on_submit():
        try:
            sql_string = db_insert(SAMPLE_TABLE,
                                   [sample_form.sample_id, sample_form.name,
                                    sample_form.generation, sample_form.sex,
                                    sample_form.mother, sample_form.father,
                                    sample_form.notes])
            g.db_cursor.execute(sql_string)
            flash(sql_string)
        except MySQLdb.IntegrityError:
            flash('ERROR: ' + sample_form.sample_id.data + ' already exists!')
        return redirect('/insert')
    elif marker_form.validate_on_submit():
        try:
            sql_string = db_insert(MARKER_TABLE,
                                   [marker_form.marker_id,
                                    marker_form.meiotic_pos,
                                    marker_form.dog_chrom,
                                    marker_form.dog_pos,
                                    marker_form.fox_seg,
                                    marker_form.fox_chrom,
                                    marker_form.fox_pos])
            g.db_cursor.execute(sql_string)
            flash(sql_string)
        except MySQLdb.IntegrityError:
            flash('ERROR: ' + marker_form.marker_id.data + ' already exists!')
        return redirect('/insert')
    return render_template('insert.html', title='Insert',
                           sample_form=sample_form, marker_form=marker_form)

@app.route('/update', methods=['GET', 'POST'])
def update():
    sample_form = UpdateSampleForm(prefix='sample_form')
    marker_form = UpdateMarkerForm(prefix='marker_form')
    if sample_form.validate_on_submit():
        sql_string = db_update(SAMPLE_TABLE, sample_form.sample_id,
                               [sample_form.new_sample_id, sample_form.name,
                                sample_form.generation, sample_form.sex,
                                sample_form.mother, sample_form.father,
                                sample_form.notes])
        g.db_cursor.execute(sql_string)
        flash(sql_string)
        return redirect('/update')
    elif marker_form.validate_on_submit():
        sql_string = db_update(MARKER_TABLE, marker_form.marker_id,
                               [marker_form.marker_id,
                                marker_form.meiotic_pos,
                                marker_form.dog_chrom,
                                marker_form.dog_pos,
                                marker_form.fox_seg,
                                marker_form.fox_chrom,
                                marker_form.fox_pos])
        g.db_cursor.execute(sql_string)
        flash(sql_string)
        return redirect('/update')
    return render_template('update.html', title='Update',
                           sample_form=sample_form, marker_form=marker_form)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    sample_form = DeleteSampleForm(prefix='sample_form')
    marker_form = DeleteMarkerForm(prefix='marker_form')
    if sample_form.validate_on_submit():
        sql_string = db_delete(SAMPLE_TABLE, sample_form.sample_id.data)
        g.db_cursor.execute(sql_string)
        flash(sql_string)
        return redirect('/delete')
    elif marker_form.validate_on_submit():
        sql_string = db_delete(MARKER_TABLE, marker_form.marker_id.data)
        g.db_cursor.execute(sql_string)
        flash(sql_string)
        return redirect('/delete')
    return render_template('delete.html', title='Delete',
                           sample_form=sample_form, marker_form=marker_form)

@app.before_request
def db_connect():
    g.db_conn = MySQLdb.connect(db=DB_NAME, host=DB_HOST, passwd=DB_PASSWD,
                                user=DB_USER)
    g.db_cursor = g.db_conn.cursor()

@app.teardown_request
def db_disconnect(exception=None):
    g.db_conn.commit()
    g.db_cursor.close()
    g.db_conn.close()
