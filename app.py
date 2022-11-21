from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,flash,g
app = Flask(__name__)
from werkzeug.exceptions import abort
from db import get_db

@app.route('/')
def indexx(page=1):
    db,c=get_db()
    c.execute('select * from publicacion where id>=%s and id<=%s',(page*10-10,page*10))
    calls=c.fetchall()
    num=len(calls)
    print(num)
    return render_template('tiak/index.html',calls=calls,num=num,page=page)

@app.route('/<int:page>')
def index(page):
    db,c=get_db()
    c.execute('select * from publicacion where id>=%s and id<=%s',(page*10-10,page*10))
    calls=c.fetchall()
    num=len(calls)/10+1
    print(num)
    return render_template('tiak/index.html',calls=calls,num=num,page=page)

@app.route('/crear',methods=('GET','POST'))
def create():
    if request.method=='POST':   
        hist=request.form['historia']
        error=None
        if not hist:
            error='historia requerida'
        if error is not None:
            flash(error)    
        else:
            db,c=get_db()
            c.execute('insert into publicacion (Comentario) values (%s)',(hist,))
            db.commit()
            return redirect(url_for('indexx')) 
        return redirect(url_for('indexx'))
    return render_template('tiak/historia.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
   app.run()