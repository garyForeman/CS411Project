from flask import render_template, flash, redirect
from app import app
from .forms import InsertForm
from flask import g
from SQLfunctions import *

@app.route('/')
@app.route('/index')
def index():
   return render_template('index.html', title='Home')

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    form = InsertForm()
    if form.validate_on_submit():
        g.db_cursor.execute(db_insert(SAMPLE_TABLE, form.sample_id.data))
        flash(db_insert(SAMPLE_TABLE, form.sample_id.data))
        return redirect('/insert')
    return render_template('insert.html', title='Insert', form=form)

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
