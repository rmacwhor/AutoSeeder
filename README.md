## AutoSeeder 

AutoSeeder is a Python script that automatically seeds Smash Ultimate tournaments
on smash.gg using a ranking algorithm based on player results from smashdata.gg.



### Required dependencies

**Requests:** https://requests.readthedocs.io/en/master/

**BeautifulSoup4:** https://www.crummy.com/software/BeautifulSoup/



### How to use

**Using this script requires a valid auth token from smash.gg.
If you do not have an auth token, you can create one from the following
link (must have a smash.gg account): https://smash.gg/admin/profile/developer**

Once you have your auth token, you must find the line starting with AUTH_TOKEN
in smash.gg and replace it with a string containing your own auth token.

In a command window, simply enter the following command on Windows:

```python autoseeder.py```

You will be prompted for the event ID and the number of entrants for the event.
You will also be asked if you want to pull seed IDs from smash.gg.
If you choose yes, you will need to provide the phase ID to seed.

**Warning: If you pull seed IDs from smash.gg, autoseeder will only seed
players that have been marked as seeded on the seeding page- any
unseeded players will not be seeded!** As such, please make sure
you mark all players that need to be seeded before choosing this option.

The event ID and phase ID can be found by going to the Brackets page as an 
admin and switching to a bracket in the phase. The IDs will be at the end of the URL like so: 

`https://smash.gg/admin/tournament/{tourney_name}/brackets/{event_id}/{phase_id}/{pool_id}`

The number of entrants is required so that all event attendees can be pulled from your event in one request.



### Known issues

- In most cases, the player's ID on smash.gg matches the player's ID on smashdata.gg.
However, there are rare instances where these IDs do not match.
As a result, autoseeder will be unable to find tournament results for this player when they actually exist.
Testing and debugging has revealed that this is due to smashdata.gg merging results
from multiple IDs into one player. Sometimes these merges are done erroneously,
and consequently two separate players' data is converged into one.


- While smashdata.gg can create tournament results for a player without a
smash.gg account, autoseeder might not find that data due to how it connects
with smash.gg. Therefore, players without smash.gg accounts are less likely to be seeded.
(Generally, this is not a real issue, since players that aren't on smash.gg
don't usually need to be seeded anyway...)
