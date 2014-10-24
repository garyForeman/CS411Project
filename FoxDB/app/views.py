from flask import render_template, flash, redirect, Response, url_for, request
from app import app
from .forms import InsertSampleForm, UpdateSampleForm, DeleteSampleForm
from .forms import InsertGenotypeForm, UpdateGenotypeForm, DeleteGenotypeForm
from .forms import InsertMarkerForm, UpdateMarkerForm, DeleteMarkerForm
from .forms import QueryForm
from flask import g
from app.SQLfunctions import DB_NAME, DB_HOST, DB_USER, DB_PASSWD
from app.SQLfunctions import db_insert, db_update, db_delete, db_query
from app.SQLfunctions import SAMPLE_TABLE, GENOTYPE_TABLE, MARKER_TABLE
import MySQLdb

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    sample_form = InsertSampleForm(prefix='sample_form')
    genotype_form = InsertGenotypeForm(prefix='genotype_form')
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
    elif genotype_form.validate_on_submit():
        try:
            sql_string = db_insert(GENOTYPE_TABLE,
                                   [genotype_form.sample_id,
                                    genotype_form.marker_id,
                                    genotype_form.genotype1,
                                    genotype_form.genotype2])
            g.db_cursor.execute(sql_string)
            flash(sql_string)
        except MySQLdb.IntegrityError:
            flash('Integrety Error: Either this key already exists, or one ' +
                  'of the key attributes does not satisfy referential ' +
                  'integrity constraint.')
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
                           sample_form=sample_form, marker_form=marker_form,
                           genotype_form=genotype_form)

@app.route('/update', methods=['GET', 'POST'])
def update():
    sample_form = UpdateSampleForm(prefix='sample_form')
    genotype_form = UpdateGenotypeForm(prefix='genotype_form')
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
    elif genotype_form.validate_on_submit():
        try:
            sql_string = db_update(GENOTYPE_TABLE,
                                   [genotype_form.sample_id,
                                    genotype_form.marker_id],
                                   [genotype_form.new_sample_id,
                                    genotype_form.new_marker_id,
                                    genotype_form.genotype1,
                                    genotype_form.genotype2])
            g.db_cursor.execute(sql_string)
            flash(sql_string)
        except MySQLdb.IntegrityError:
            flash('ERROR: one of the new key values does not satisfy ' +
                  'referential integrity constraint.')
        return redirect('/update')
    elif marker_form.validate_on_submit():
        sql_string = db_update(MARKER_TABLE, marker_form.marker_id,
                               [marker_form.new_marker_id,
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
                           sample_form=sample_form, marker_form=marker_form,
                           genotype_form=genotype_form)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    sample_form = DeleteSampleForm(prefix='sample_form')
    genotype_form = DeleteGenotypeForm(prefex='genotype_form')
    marker_form = DeleteMarkerForm(prefix='marker_form')
    if sample_form.validate_on_submit():
        sql_string = db_delete(SAMPLE_TABLE, sample_form.sample_id.data)
        g.db_cursor.execute(sql_string)
        flash(sql_string)
        return redirect('/delete')
    elif genotype_form.validate_on_submit():
        sql_string = db_delete(GENOTYPE_TABLE, [genotype_form.sample_id.data,
                                                genotype_form.marker_id.data])
        g.db_cursor.execute(sql_string)
        flash(sql_string)
        return redirect('/delete')
    elif marker_form.validate_on_submit():
        sql_string = db_delete(MARKER_TABLE, marker_form.marker_id.data)
        g.db_cursor.execute(sql_string)
        flash(sql_string)
        return redirect('/delete')
    return render_template('delete.html', title='Delete',
                           sample_form=sample_form, marker_form=marker_form,
                           genotype_form=genotype_form)

@app.route('/query', methods=['GET', 'POST'])
def query():
    form = QueryForm()
    if form.validate_on_submit():
        sql_string = db_query([form.sample_all.data,
                               form.sample_sample_id.data,
                               form.sample_name.data,
                               form.sample_generation.data,
                               form.sample_sex.data,
                               form.sample_mother.data,
                               form.sample_father.data,
                               form.sample_notes.data,
                               form.genotype_all.data,
                               form.genotype_sample_id.data,
                               form.genotype_marker_id.data,
                               form.genotype_genotype1.data,
                               form.genotype_genotype2.data,
                               form.marker_all.data,
                               form.marker_marker_id.data,
                               form.marker_meiotic_pos.data,
                               form.marker_dog_chrom.data,
                               form.marker_dog_pos.data,
                               form.marker_fox_seg.data,
                               form.marker_fox_chrom.data,
                               form.marker_fox_pos.data],
                              form.where_clause.data)
        if sql_string == 1:
            flash('WARNING: Empty Query')
            return redirect('/query')
        elif sql_string == 2:
            flash('Query disallowed: query for samples and markers separately')
            return redirect('/query')
        else:
            try:
                #flash(sql_string)
                #return redirect('/query')
                g.db_cursor.execute(sql_string)
                data = g.db_cursor.fetchall()
                data_list = []
                for row in data:
                    data_list.append(','.join(str(i) for i in row) + '\n')
                def generate():
                    for row in data_list:
                        yield row
                return Response(generate(), mimetype='text')
            except MySQLdb.ProgrammingError:
                flash('ERROR: your query contained invalid syntax')
                return redirect('/query')
    return render_template('query.html', title='Query', form=form)

@app.route('/query/result', methods=['GET', 'POST'])
def generate_csv():
    data = request.args.getlist('data')
    def generate():
        for row in data:
            yield row
    return Response(generate(), mimetype='text')

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
