from findahouse import app
from flask import session, g, escape, redirect, url_for, render_template,\
                                request, Flask, Response, abort, jsonify
from flask_login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user 
from flask_sqlalchemy import SQLAlchemy
from gestion_db import Departement

db = SQLAlchemy(app)

app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx')

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "identification"


# silly user model
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = str(id)
        self.password =  str(id)
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


# create some users with ids 1 to 20       
#users = User('pierre') 


def active_page(page):
    '''Use to select the active html page'''
    html_page = {'identification': '', 'inscription': '', 'geoinformation': '', 'contact': '', 'espace_personnel': ''}
    html_page[page] = ' class=active'
    return html_page

@app.route('/geodata')
def geodata():
    #departement = Departement.query.all(numero_departement = '77').first()
    print "test"
    departement = Departement.query.filter_by(numero_departement = '64').first()
    #departement = Departement.query.all()  
    #print departement[0].numero_departement
    return jsonify(departement.limite_departement)


@app.route('/contact')
def contact():
    g.active_page = active_page('contact')
    return render_template('contact.html')

@app.route('/geoinformation')
def geoinformation():
    g.active_page = active_page('geoinformation')
    return render_template('geoinformation.html')

@app.route('/inscription')
def inscription():
    g.active_page = active_page('inscription')
    return render_template('inscription.html')


@app.route('/espace_personnel')
@login_required
def espace_personnel():
    g.active_page = active_page('espace_personnel')
    return render_template('espace_personnel.html')
 
# somewhere to login
@app.route("/identification", methods=["GET", "POST"])
def identification():
    g.active_page = active_page('identification')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']        
        if password == 'pierre':
            user = User(id)
            login_user(user)
            return redirect(request.args.get("next") or url_for('geoinformation'))
        else:
            return abort(401)
    else:
        return render_template('identification.html')
        #return Response('''
        #<form action="" method="post">
        #    <p><input type=text name=username>
        #    <p><input type=password name=password>
        #    <p><input type=submit value=Login>
        #</form>
        #''')


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')
    
    
# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid)
 


