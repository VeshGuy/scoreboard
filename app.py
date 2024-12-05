from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from webforms import LoginForm, NamerForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = "secret key"

db = SQLAlchemy(app)


class TeamsInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Integer, nullable=True)    

    def __repr__(self):
        return '<Name %r>' % self.score
    
with app.app_context():
        db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm()
    namelist = ['Pranav', 'Sarvesh', 'Meghna', 'Samay']
    passw = "EPOCH@123"
    if request.method=='POST':
        if request.form['name'] in namelist and request.form['password'] == passw:
            return redirect(url_for('teams'))
    return render_template('index.html', form=form)

@app.route('/teams', methods=['GET', 'POST'])
def teams():
    team = NamerForm()
    if team.validate_on_submit():
        user = TeamsInfo.query.filter_by(name=team.name.data).first()
        if user is None:
            user = TeamsInfo(name=team.name.data, score=team.score.data)
            db.session.add(user)
            db.session.commit()
            flash('Team Added Successfully!')
        else:
            flash('Team Already Exists!')
        team.name.data=''
        team.score.data=0
    our_users = TeamsInfo.query.order_by(TeamsInfo.score)
    return render_template("teams.html", form=team, users=our_users)


@app.route('/update/<team_id>', methods=['GET', 'POST'])
def update_team(team_id):
    team = NamerForm()
    user = TeamsInfo.query.filter_by(id=team_id).first()

    if user is not None:
        if team.validate_on_submit():

            user.name = team.name.data
            user.score = team.score.data
            db.session.commit()
            flash('Team Updated Successfully!')
            return redirect(url_for('teams'))
        else:
            team.name.data = user.name
            team.score.data = user.score

    our_users = TeamsInfo.query.order_by(TeamsInfo.score)
    return render_template("teams.html", form=team, users=our_users)


@app.route('/delete/<team_id>', methods=['get', 'post'])
def delete_team(team_id):
    team = NamerForm()
    user = TeamsInfo.query.filter_by(id=team_id).first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        flash('Team Deleted')
        our_users = TeamsInfo.query.order_by(TeamsInfo.score)
        return redirect(url_for('teams'))
    return render_template("teams.html", form=team, users=our_users)

@app.route('/scoreboard', methods=['GET', 'POST'])
def score_board():
    our_users = TeamsInfo.query.all()
    return render_template('scoreboard.html', users=our_users)

if __name__=='__main__':
    app.run(debug=True)