## AutoSeeder 

AutoSeeder is a Python script that automatically seeds smash.gg tournaments 
using a ranking algorithm based on player results from smashdata.gg.

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
The event ID can be found by going to the Events page as an admin and 
clicking on the event name. The ID will be at the end of the URL like so: 

`https://smash.gg/admin/tournament/{tournament-name}/event-edit/{event-id}`

The number of entrants is required so that all event attendees can be pulled from your event in one request.