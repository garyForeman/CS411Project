from flask import render_template, flash, redirect
from app import app
from .forms import InsertForm, DeleteForm
from flask import g
from SQLfunctions import DB_NAME, DB_HOST, DB_USER, DB_PASSWD
from SQLfunctions import SAMPLE_TABLE
from SQLfunctions import db_insert, db_delete
import MySQLdb

@app.route('/')
@app.route('/index')
def index():
   return render_template('index.html', title='Home')

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    form = InsertForm()
    if form.validate_on_submit():
        #g.db_cursor.execute(db_insert(SAMPLE_TABLE, form.sample_id.data))
        #flash(db_insert(SAMPLE_TABLE, form.sample_id.data))
        flash("sample_id=" + str(form.sample_id.data))# + ", name=" + form.name.data)# +
             # ", generation=" + form.generation.data + ", mother=" +
             # form.mother.data + ", father=" + form.father.data)# + ", notes=" +
              #form.notes.data + ", sex=" + form.sex.data)
        return redirect('/insert')
    return render_template('insert.html', title='Insert', form=form)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
   form = DeleteForm()
   if form.validate_on_submit():
      g.db_cursor.execute(db_delete(SAMPLE_TABLE, form.sample_id.data))
      g.db_conn.commit()
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
   g.db_cursor.close()
   g.db_conn.close()
