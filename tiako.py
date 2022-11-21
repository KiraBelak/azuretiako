from flask import(
    Blueprint,flash,g,redirect,render_template,request,url_for
)
from werkzeug.exceptions import abort
from db import get_db

bp=Blueprint('tiako',__name__)

@bp.route('/')
def indexx(page=1):
    db,c=get_db()
    c.execute('select * from publicacion where id>=%s and id<=%s',(page*10-10,page*10))
    calls=c.fetchall()
    num=len(calls)
    print(num)
    return render_template('tiak/index.html',calls=calls,num=num,page=page)

@bp.route('/<int:page>')
def index(page):
    db,c=get_db()
    c.execute('select * from publicacion where id>=%s and id<=%s',(page*10-10,page*10))
    calls=c.fetchall()
    num=len(calls)/10+1
    print(num)
    return render_template('tiak/index.html',calls=calls,num=num,page=page)

@bp.route('/crear',methods=('GET','POST'))
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
            return redirect(url_for('tiako.indexx')) 
        return redirect(url_for('tiako.indexx'))
    return render_template('tiak/historia.html')