# Create Your Own NBA Team - a web app developed using Python and Flask

![app screenshot](https://raw.githubusercontent.com/joshwalk/364final/master/screenshot.jpg)

My application allows the user to add NBA teams and players to a database. Once they are added, the user can create custom teams from the stored players. The user has the ability to delete a player and also to rename a custom team after creation. There is a function allowing users to search for saved players as well.

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