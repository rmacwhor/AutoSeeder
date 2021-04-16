## AutoSeeder 

AutoSeeder is a Python script that automatically seeds Smash Ultimate tournaments
on smash.gg using a ranking algorithm based on player results from smashdata.gg.

It should be noted that this is not meant to be a perfect seeder- no seeding
is perfect, after all. No matter how advanced I make the ranking algorithm
in this program, it won't be able to consider external factors such as 
schedule conflicts and playing your best friend round 1. However, I hope
this tool will find some use in initial drafts of seeding or in seeding
pools of players you are unfamiliar with.

For those curious, you can read about my process for creating a seeding algorithm here: https://docs.google.com/document/d/1V0Y3W1SJ7TbQIijofi4luB-PwVgfypRvQCixeDehc4M/edit?usp=sharing



### Required dependencies

**Requests:** https://requests.readthedocs.io/en/master/

**BeautifulSoup4:** https://www.crummy.com/software/BeautifulSoup/

**lxml:** https://lxml.de/



### How to use

**Using this script requires a valid auth token from smash.gg.
If you do not have an auth token, you can create one from the following
link (must have a smash.gg account): https://smash.gg/admin/profile/developer**

Once you have your auth token, you must find the line starting with AUTH_TOKEN
in smash.gg and replace it with a string containing your own auth token.

In a command window, simply enter the following command on Windows:

```python autoseeder.py```

You will be prompted for the event ID and the number of entrants for the event.
You will also be asked if you want to automatically apply these seed changes to smash.gg.
If you choose yes, you will need to provide the phase ID to seed.
Either way, the program will print out a list of seeds in order of ranking, including player scores.

**Warning: If you automatically apply seed changes, autoseeder will only seed
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

- Players with certain unusual characters in their tags (Ø, for example) cause errors on smashdata.gg;
attempting to search for these players will result in a 500 Internal Server Error.
As such, these players will end up unseeded.

- While smashdata.gg can create tournament results for a player without a
smash.gg account, autoseeder might not find that data due to how it connects
with smash.gg. Therefore, players without smash.gg accounts are less likely to be seeded.
(Generally, this is not a real issue, since players that aren't on smash.gg
don't usually need to be seeded anyway...)
