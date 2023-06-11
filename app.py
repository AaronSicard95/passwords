from flask import Flask, render_template, redirect,session
from forms import RegisterForm, LogInForm, FeedbackForm
from models import db,User,connect_db, Feedback

app = Flask(__name__)
app.config['SECRET_KEY']='MAMAMIA'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///users"

connect_db(app)
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def root():
    if session.get('userid'):
        user=User.query.get(session.get('userid'))
        return redirect(f'/users/{user.username}')
    else:
        return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        new_user.password = new_user.register(username,password)
        db.session.add(new_user)
        db.session.commit()
        session['userid'] = new_user.id
        return redirect(f'/users/{username}')
    else:
        return render_template('/register.html', form=form)
    
@app.route('/secret')
def secret():
    
    if session.get('userid'):
        user = User.query.get(session['userid'])
        return render_template('/secret.html', loggedin=True, password = user.password)
    else:
        return redirect('/')
    
@app.route('/logout')
def logout():
    if session.get('userid'):
        session.pop('userid')
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user:
            if user.authenticate(user.username,password):
                session['userid']=user.id
                return redirect(f'/users/{username}')
        else:
            form.username.errors = ['invalid username or password']
    return render_template('/register.html', form=form)

@app.route('/users/<string:username>')
def showUser(username):
    user = User.query.filter_by(username=username).first()
    return render_template('user.html', user=user, loggeduser=session.get('userid'))
    
@app.route('/users/<string:username>/delete')
def deleteUser(username):
    user = User.query.filter_by(username=username).first()
    if user:
        if user.id == session.get('userid'):
            db.session.delete(user)
            db.session.commit()
            session.pop('userid')
            return redirect('/')
        else:
            return redirect(f'/users/{username}')
    else:
        return redirect(f'/')
    
@app.route('/users/<string:username>/feedback/add', methods=['GET', 'POST'])
def addFeedback(username):
    user = User.query.filter_by(username=username).first()
    form = FeedbackForm()
    if session.get('userid')==user.id:
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            new_post = Feedback(
                title=title,
                content=content,
                username=username
            )
            db.session.add(new_post)
            db.session.commit()
            return redirect(f'/users/{username}')
        else:
            return render_template('register.html', form=form)
    return redirect(f'/users/{username}')

@app.route('/feedback/<int:feedbackid>/update', methods=['GET', 'POST'])
def updateFeedback(feedbackid):
    feedback = Feedback.query.get(feedbackid)
    form = FeedbackForm(obj=feedback)
    if session.get('userid')==feedback.user.id:
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            feedback.title=title
            feedback.content=content
            db.session.add(feedback)
            db.session.commit()
            return redirect(f'/users/{feedback.username}')
        else:
            return render_template('register.html', form=form)
    return redirect(f'/users/{feedback.username}')

@app.route('/feedback/<int:feedbackid>/delete', methods=['GET', 'POST'])
def deleteFeedback(feedbackid):
    feedback = Feedback.query.get(feedbackid)
    if session.get('userid')==feedback.user.id:
        username=feedback.username
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/users/{username}',)
    else:
        return redirect(f'/users/{feedback.username}')