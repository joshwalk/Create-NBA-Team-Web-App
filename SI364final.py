import os
import requests
import json
from flask import Flask, render_template, session, redirect, request, url_for, flash
from flask_script import Manager, Shell
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, PasswordField, BooleanField, SelectMultipleField, ValidationError, SelectField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash, check_password_hash

# Imports for login management
from flask_login import LoginManager, login_required, logout_user, login_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Application configurations
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hardtoguessstring'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or "postgresql://localhost/joshwalkfinaldb"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# App addition setups
manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# Login configurations setup
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

# The following static data was retrieved from the nba.py project (https://github.com/seemethere/nba_py)
team_choices = [('1610612737', 'Atlanta Hawks'),
 ('1610612738', 'Boston Celtics'),
 ('1610612751', 'Brooklyn Nets'),
 ('1610612766', 'Charlotte Hornets'),
 ('1610612741', 'Chicago Bulls'),
 ('1610612739', 'Cleveland Cavaliers'),
 ('1610612742', 'Dallas Mavericks'),
 ('1610612743', 'Denver Nuggets'),
 ('1610612765', 'Detroit Pistons'),
 ('1610612744', 'Golden State Warriors'),
 ('1610612745', 'Houston Rockets'),
 ('1610612754', 'Indiana Pacers'),
 ('1610612746', 'Los Angeles Clippers'),
 ('1610612747', 'Los Angeles Lakers'),
 ('1610612763', 'Memphis Grizzlies'),
 ('1610612748', 'Miami Heat'),
 ('1610612749', 'Milwaukee Bucks'),
 ('1610612750', 'Minnesota Timberwolves'),
 ('1610612740', 'New Orleans Pelicans'),
 ('1610612752', 'New York Knicks'),
 ('1610612760', 'Oklahoma City Thunder'),
 ('1610612753', 'Orlando Magic'),
 ('1610612755', 'Philadelphia Sixers'),
 ('1610612756', 'Phoenix Suns'),
 ('1610612757', 'Portland Trail Blazers'),
 ('1610612758', 'Sacramento Kings'),
 ('1610612759', 'San Antonio Spurs'),
 ('1610612761', 'Toronto Raptors'),
 ('1610612762', 'Utah Jazz'),
 ('1610612764', 'Washington Wizards')]
headers = {
    'user-agent': ('Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'),
    'Dnt': ('1'),
    'Accept-Encoding': ('gzip, deflate, sdch'),
    'Accept-Language': ('en'),
    'origin': ('http://stats.nba.com')
    }

# Association tables
user_collection = db.Table('user_collection',db.Column('player_id', db.Integer, db.ForeignKey('players.id')),db.Column('collection_id',db.Integer, db.ForeignKey('personalPlayerCollections.id')))

########################
######## Models #########
########################

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    collection = db.relationship('PersonalPlayerCollection', backref='User')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

## DB load function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) # returns User object or None


class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))

    def __repr__(self):
        return "{}, Jersey No.: {}".format(self.name,str(self.jersey_no))


# Model to store a personal player collection
class PersonalPlayerCollection(db.Model):
    __tablename__ = "personalPlayerCollections"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    players = db.relationship('Player',secondary=user_collection,backref=db.backref('personalPlayerCollections',lazy='dynamic'),lazy='dynamic')


class Team(db.Model):
    __tablename__ = "teams"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128),unique=True)
    player = db.relationship('Player', backref='Team')

    def __repr__(self):
        return self.name

########################
######## Forms #########
########################

# Provided
class RegistrationForm(FlaskForm):
    email = StringField('Email:', validators=[Required(),Length(1,64),Email()])
    username = StringField('Username:',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password:',validators=[Required(),EqualTo('password2',message="Passwords must match")])
    password2 = PasswordField("Confirm Password:",validators=[Required()])
    submit = SubmitField('Register User')

    #Additional checking methods for the form
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')

# Provided
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

# class GifSearchForm(FlaskForm):
#     search = StringField("Enter a term to search GIFs", validators=[Required()])
#     submit = SubmitField('Submit')

class TeamSelectForm(FlaskForm):
    team_select = SelectField('Select team')
    # player_select = SelectMultipleField('Select players to add')
    submit = SubmitField("Continue")

class PlayerSelectForm(FlaskForm):
    player_select = SelectMultipleField('Select player(s)')
    submit = SubmitField("Add players")

########################
### Helper functions ###
########################

def get_players_from_team(team_api_id):
    base_url = 'http://stats.nba.com/stats/commonteamroster/?Season=2017-18&TeamID='
    response = requests.get(base_url + str(team_api_id), headers=headers)
    data = json.loads(response.text)
    return [x[3] for x in data['resultSets'][0]['rowSet']]

def get_or_create_player(db_session, name, team_id):
    player = db_session.query(Player).filter_by(name = name).first()
    if player:
        return player
    else:
        player = Player(name = name, team_id=team_id)
        db_session.add(player)
        db_session.commit()
        return player

def get_or_create_team(db_session, name):
    team = db_session.query(Team).filter_by(name = name).first()
    if team:
        return team
    else:
        team = Team(name = name)
        db_session.add(team)
        db_session.commit()
        return team


########################
#### View functions ####
########################

## Error handling routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


## Login-related routes
@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))

@app.route('/register',methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now log in!')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

## other routes
@app.route('/', methods=['GET', 'POST'])
def index():
    team_form = TeamSelectForm()
    team_form.team_select.choices = team_choices
    # if team_form.validate_on_submit()
    #     team_selected = team_form.team_select.data
    #     team_selected_name = dict(team_choices)[str(team_selected)]
    #     new_team = get_or_create_team(db.session, team_selected_name)
    #     players_from_team = get_players_from_team(int(team_selected))
    #     player_form.player_select.choices = [(x,x) for x in players_from_team]
    #     return redirect(url_for('player_select'))
    return render_template('index.html',team_form=team_form)

@app.route('/player_select', methods=['GET', 'POST'])
def player_select():
    if request.args:
        team_selected = request.args.get('team_select')
    team_selected_name = dict(team_choices)[str(team_selected)]
    new_team = get_or_create_team(db.session, team_selected_name)
    players_from_team = get_players_from_team(int(team_selected))

    player_form = PlayerSelectForm()
    player_form.player_select.choices = [(x,x) for x in players_from_team]
    if player_form.validate_on_submit():
        print(player_form.player_select.data)
        for p in player_form.player_select.data:
            get_or_create_player(db.session, p, new_team.id)
    return render_template('player_select.html',player_form=player_form, team_selected_name=team_selected_name)


@app.route('/all_players')
def all_players():
    player_team_list = []
    for player in Player.query.all():
        name = player.name
        team = Team.query.filter_by(id=player.team_id).first().name
        name_team = name + ", " + team
        player_team_list.append(name_team)
    return render_template('all_players.html', player_team_list=player_team_list)

@app.route('/all_teams')
def all_teams():
    teams = Team.query.all()
    return render_template('all_teams.html', teams=teams)


if __name__ == '__main__':
    db.create_all()
    manager.run()
