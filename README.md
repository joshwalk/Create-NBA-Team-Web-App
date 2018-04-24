# Joshua Walker SI 364 Final project

## Description
My application allows the user to add NBA teams and players to a database. Once they are added, the user can create custom teams from the stored players. The user has the ability to delete a player and also to rename a custom team after creation. There is a function allowing users to search for saved players as well.

## Explanation of how a user can use the running application
To get the program running, first create a database titled `joshwalkfinaldb`. Then run `python SI364final.py runserver` from within the directory. Follow the link on the top of the page to sign in/register.

The home page is where you can add a team/player to the database. Select a team from the drop-down menu and press Continue. That team is now added to the database, and you are brought to a page that lists all of the players from that team. From the multiple select field, choose player(s) and press Add players to add these players to the database. For example, select "Cleveland Cavaliers" as the team and select "LeBron James," "Kevin Love," and "Kyle Korver" for the players.

From the navigation, you can select from the various options including see all saved teams or players, and search for all saved players. On the "See all saved players" page you have the ability for each player to delete from the db. To create a custom team, select the appropriate link, and on the page that appears enter a custom team name and select players (at least 2) that are saved to the db you'd like to add to your team and press Create team. You are then brought to the "View your custom teams" page. You are given the option for each custom team to rename it. To do so, select "Rename," enter the new name and press "update name."

## Modules to install
There are no additional modules to install.

## List of routes
`/login` -> `login.html`

`/logout` -> logs out user and redirects to index page

`/register` -> `register.html`

`/` -> `index.html`

`/player_select` -> `player_select.html`

`/all_players` -> `all_players.html`

`/all_teams` -> `all_teams.html`

`/player_search` -> `player_search.html`

`/new_custom_team` -> `new_custom_team.html`

`/custom_teams` -> `custom_teams.html`

`/custom_team/<id_num>` -> `custom_team.html`

`/update/<custom_team_id>` -> `update_team.html`

`/delete/<player_id>` -> deletes a player and redirects to all_players page



## Requirements checklist
- [ ] **Ensure that your `SI364final.py` file has all the setup (`app.config` values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on `http://localhost:5000` (and the other routes you set up). **Your main file must be called** `SI364final.py`**, but of course you may include other files if you need.****

- [ ] **A user should be able to load `http://localhost:5000` and see the first page they ought to see on the application.**

- [ ] **Include navigation in `base.html` with links (using `a href` tags) that lead to every other page in the application that a user should be able to click on. (e.g. in the lecture examples from the Feb 9 lecture, [like this](https://www.dropbox.com/s/hjcls4cfdkqwy84/Screenshot%202018-02-15%2013.26.32.png?dl=0) )**

- [ ] **Ensure that all templates in the application inherit (using template inheritance, with `extends`) from `base.html` and include at least one additional `block`.**

- [ ] **Must use user authentication (which should be based on the code you were provided to do this e.g. in HW4).**

- [ ] **Must have data associated with a user and at least 2 routes besides `logout` that can only be seen by logged-in users.**

- [ ] **At least 3 model classes *besides* the `User` class.**

- [ ] **At least one one:many relationship that works properly built between 2 models.**

- [  ]**At least one many:many relationship that works properly built between 2 models.**

- [ ] **Successfully save data to each table.**

- [ ] **Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for) and use it to effect in the application (e.g. won't count if you make a query that has no effect on what you see, what is saved, or anything that happens in the app).**

- [ ] **At least one query of data using an `.all()` method and send the results of that query to a template.**

- [ ] **At least one query of data using a `.filter_by(...` and show the results of that query directly (e.g. by sending the results to a template) or indirectly (e.g. using the results of the query to make a request to an API or save other data to a table).**

- [ ] **At least one helper function that is *not* a `get_or_create` function should be defined and invoked in the application.**

- [ ] **At least two `get_or_create` functions should be defined and invoked in the application (such that information can be saved without being duplicated / encountering errors).**

- [ ] **At least one error handler for a 404 error and a corresponding template.**

- [ ] **At least one error handler for any other error (pick one -- 500? 403?) and a corresponding template.**

- [ ] **Include at least 4 template `.html` files in addition to the error handling template files.**

  - [ ] **At least one Jinja template for loop and at least two Jinja template conditionals should occur amongst the templates.**

- [ ] **At least one request to a REST API that is based on data submitted in a WTForm OR data accessed in another way online (e.g. scraping with BeautifulSoup that *does* accord with other involved sites' Terms of Service, etc).**

  - [ ] **Your application should use data from a REST API or other source such that the application processes the data in some way and saves some information that came from the source *to the database* (in some way).**

- [ ] **At least one WTForm that sends data with a `GET` request to a *new* page.**

- [ ] **At least one WTForm that sends data with a `POST` request to the *same* page. (NOT counting the login or registration forms provided for you in class.)**

- [ ] **At least one WTForm that sends data with a `POST` request to a *new* page. (NOT counting the login or registration forms provided for you in class.)**

- [ ] **At least two custom validators for a field in a WTForm, NOT counting the custom validators included in the log in/auth code.**

- [ ] **Include at least one way to *update* items saved in the database in the application (like in HW5).**

- [ ] **Include at least one way to *delete* items saved in the database in the application (also like in HW5).**

- [ ] **Include at least one use of `redirect`.**

- [ ] **Include at least two uses of `url_for`. (HINT: Likely you'll need to use this several times, really.)**

- [ ] **Have at least 5 view functions that are not included with the code we have provided. (But you may have more! *Make sure you include ALL view functions in the app in the documentation and navigation as instructed above.*)**

- [ ] (100 points) Include a use of an AJAX request in your application that accesses and displays useful (for use of your application) data.
- [ ]  **(100 points) Create, run, and commit at least one migration.**
- [ ] (100 points) Include file upload in your application and save/use the results of the file. (We did not explicitly learn this in class, but there is information available about it both online and in the Grinberg book.)
- [ ]  (100 points) Deploy the application to the internet (Heroku) — only counts if it is up when we grade / you can show proof it is up at a URL and tell us what the URL is in the README. (Heroku deployment as we taught you is 100% free so this will not cost anything.)
- [ ]  (100 points) Implement user sign-in with OAuth (from any other service), and include that you need a *specific-service* account in the README, in the same section as the list of modules that must be installed.
