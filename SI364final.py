# Joshua Walker
# SI 364 Final Project

# Note: import statements, app configurations, and login configuration/setup and User models/functionality copied from provided code in HW4
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
import re

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

manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# Login configurations setup
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

# The following static data was retrieved and modified from the nba.py project (https://github.com/seemethere/nba_py)
# The code I wrote to put the team choices together is in final_notes.ipynb
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
# The header data allows for the successful request to the NBA Stats API, copied from aforementioned nba.py project
headers = {
    'user-agent': ('Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'),
    'Dnt': ('1'),
    'Accept-Encoding': ('gzip, deflate, sdch'),
    'Accept-Language': ('en'),
    'origin': ('http://stats.nba.com')
    }

# Association tables
# This association table, user_teams, connects the customTeams table with the players table to form a many-to-many relationship
user_teams = db.Table('user_teams',db.Column('player_id', db.Integer, db.ForeignKey('players.id')),db.Column('custom_team_id',db.Integer, db.ForeignKey('customTeams.id')))

########################
######## Models #########
########################

# users table has a one-to-many relationship with customTeams
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    collection = db.relationship('CustomTeam', backref='User')

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
        return self.name

# teams table has a one-to-many relationship with players
class Team(db.Model):
    __tablename__ = "teams"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128),unique=True)
    player = db.relationship('Player', backref='Team')

    def __repr__(self):
        return self.name

class CustomTeam(db.Model):
    __tablename__ = "customTeams"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    players = db.relationship('Player',secondary=user_teams,backref=db.backref('customTeams',lazy='dynamic'),lazy='dynamic')


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

class TeamSelectForm(FlaskForm):
    team_select = SelectField('Select team')
    submit = SubmitField("Continue")

class PlayerSelectForm(FlaskForm):
    player_select = SelectMultipleField('Select player(s)')
    submit = SubmitField("Add players")

def capitalized_check(form, field):
    if not re.findall(r'[A-Z][a-z]+', field.data):
        raise ValidationError('First/last name must begin with capital letter')

class PlayerSearchForm(FlaskForm):
    player_search = StringField('Enter first and/or last name', validators=[Required(), capitalized_check])
    submit = SubmitField("Search")

def more_than_one_check(form, field):
    if len(field.data) < 2:
        raise ValidationError('Must choose at least 2 players')

class NewCustomTeamForm(FlaskForm):
    name = StringField('Custom team name')
    player_list = SelectMultipleField('Select at least 2 players to add to team', validators=[Required(), more_than_one_check])
    submit = SubmitField("Create team")

class UpdateButton(FlaskForm):
    submit = SubmitField("Rename")

class UpdateForm(FlaskForm):
    name = StringField('Name', validators=[Required()])
    submit = SubmitField('Update name')

class DeleteButton(FlaskForm):
    submit = SubmitField('Delete')

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

def get_or_create_custom_team(db_session, name, current_user, selected_players=[]):
    customTeam = db_session.query(CustomTeam).filter_by(name=name,user_id=current_user.id).first()
    if customTeam:
        return customTeam
    else:
        customTeam = CustomTeam(name=name, user_id=current_user.id,players=[])
        for player in selected_players:
            customTeam.players.append(player)
        db_session.add(customTeam)
        db_session.commit()
        return customTeam

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
    form = TeamSelectForm()
    form.team_select.choices = team_choices
    if form.validate_on_submit():
        team_selected = form.team_select.data
        team_selected_name = dict(team_choices)[str(team_selected)]
        new_team = get_or_create_team(db.session, team_selected_name)
        players_from_team = get_players_from_team(int(team_selected))
        player_form.player_select.choices = [(x,x) for x in players_from_team]
        return redirect(url_for('player_select'))
    return render_template('index.html',form=form)

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
        return redirect(url_for('all_players'))
    return render_template('player_select.html',player_form=player_form, team_selected_name=team_selected_name)


@app.route('/all_players')
def all_players():
    form = DeleteButton()
    player_team_list = Player.query.all()
    return render_template('all_players.html', form=form, player_team_list=player_team_list)

@app.route('/all_teams')
def all_teams():
    teams = Team.query.all()
    return render_template('all_teams.html', teams=teams)

@app.route('/player_search', methods= ['POST','GET'])
def player_search():
    results = []
    search_form = PlayerSearchForm()
    if search_form.validate_on_submit():
        print('hey')
        query = search_form.player_search.data
        results = Player.query.filter(Player.name.contains(query)).all()

    errors = [v for v in search_form.errors.values()]
    if len(errors) > 0:
        flash("Error in form submission - " + str(errors))
    return render_template('player_search.html', form=search_form, results=results)

@app.route('/new_custom_team',methods=["GET","POST"])
@login_required
def create_custom_team():
    form = NewCustomTeamForm()
    players = Player.query.all()
    form.player_list.choices = [(str(p),str(p)) for p in players]
    if form.validate_on_submit():
        name = form.name.data
        player_list_selected = form.player_list.data
        if player_list_selected:
            player_objects = [Player.query.filter_by(name=p_name).first() for p_name in player_list_selected]
            get_or_create_custom_team(db_session=db.session, name=name, current_user=current_user, selected_players=player_objects)
            return redirect(url_for('custom_teams'))

    errors = [v for v in form.errors.values()]
    if len(errors) > 0:
        flash("Error in form submission - " + str(errors))
    return render_template('new_custom_team.html', form=form)

@app.route('/custom_teams',methods=["GET","POST"])
@login_required
def custom_teams():
    form = UpdateButton()
    custom_teams = CustomTeam.query.filter_by(user_id = current_user.id).all()
    return render_template('custom_teams.html', custom_teams=custom_teams, form=form)

@app.route('/custom_team/<id_num>')
def custom_team(id_num):
    id_num = int(id_num)
    custom_team = CustomTeam.query.filter_by(id=id_num).first()
    players = custom_team.players.all()
    return render_template('custom_team.html',custom_team=custom_team, players=players)

@app.route('/update/<custom_team_id>',methods=["GET","POST"])
def update(custom_team_id):
    form = UpdateForm()
    if request.method == 'POST':
        name = form.name.data
        custom_team = CustomTeam.query.filter_by(id=custom_team_id).first()
        if custom_team:
            custom_team.name = name
            db.session.commit()
            return redirect(url_for('custom_teams'))
    return render_template('update_team.html', form=form)


@app.route('/delete/<player_id>',methods=["GET","POST"])
def delete(player_id):
    if request.method == "POST":
        player = Player.query.filter_by(id=int(player_id)).first()
        if player:
            name = player.name
            db.session.delete(player)
            db.session.commit()
            flash("Player deleted: {}".format(name))
            return redirect(url_for('all_players'))

if __name__ == '__main__':
    db.create_all()
    manager.run()
