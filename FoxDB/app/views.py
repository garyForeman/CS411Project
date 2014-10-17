from flask import render_template, flash, redirect
from app import app
from .forms import UpdateForm

@app.route('/')
@app.route('/index')
def index():
   return render_template('index.html', title='Home')

@app.route('/update', methods=['GET', 'POST'])
def update():
    form = UpdateForm()
    if form.validate_on_submit():
        flash('Sampe ID = %s' % form.sample_id.data)
        return redirect('/index')
    return render_template('update.html', title='Update', form=form)
