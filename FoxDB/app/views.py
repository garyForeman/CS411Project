from flask import render_template, flash, redirect
from app import app
from .forms import InsertForm, UpdateForm, DeleteForm
from flask import g
from SQLfunctions import DB_NAME, DB_HOST, DB_USER, DB_PASSWD
from SQLfunctions import SAMPLE_TABLE
from SQLfunctions import db_insert, db_update, db_delete
import MySQLdb

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    form = InsertForm()
    if form.validate_on_submit():
        try:
            g.db_cursor.execute(db_insert(SAMPLE_TABLE, 
                                          [form.sample_id, form.name, 
                                           form.generation, form.sex,
                                           form.mother, form.father,
                                           form.notes]))
            flash(db_insert(SAMPLE_TABLE, 
                            [form.sample_id, form.name, form.generation,
                             form.sex, form.mother, form.father, form.notes]))
        except MySQLdb.IntegrityError:
            flash('ERROR: ' + form.sample_id.data + ' already exists!')
        return redirect('/insert')
    return render_template('insert.html', title='Insert', form=form)

@app.route('/update', methods=['GET', 'POST'])
def update():
    form = UpdateForm()
    if form.validate_on_submit():
        g.db_cursor.execute(db_update(SAMPLE_TABLE, form.sample_id,
                                      [form.new_sample_id, form.name, 
                                       form.generation, form.sex,form.mother,
                                       form.father, form.notes]))
        flash(db_update(SAMPLE_TABLE, form.sample_id,
                        [form.new_sample_id, form.name, form.generation,
                         form.sex, form.mother, form.father, form.notes]))
        return redirect('/update')
    return render_template('update.html', title='Update', form=form)
        
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    form = DeleteForm()
    if form.validate_on_submit():
        g.db_cursor.execute(db_delete(SAMPLE_TABLE, form.sample_id.data))
        flash(db_delete(SAMPLE_TABLE, form.sample_id.data))
        return redirect('/delete')
    return render_template('delete.html', title='Delete', form=form)

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
