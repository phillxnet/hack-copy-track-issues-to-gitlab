What
=====

 This script migrates Trac Tickets to Gitlab Issues.

Features
--------
 * Trac Components & Ticket-Types are converted to Gitlab Labels
 * Milestones are created in Gitlab from fixture data manualy grabbed from trac (copy/paste)
 * Comments to Trac Tickets are copied over to their respective Gitlab Issues
 * Wiki Syntax in comments/descriptions is sanitized for my basic usage


How
====

 Usage: configure the following variables in ```migrate.py```` and run it (```python migrate.py```). Make sure you test it on a test project prior, if you run it twice against the same project you will get duplicated issues.

Source
-------

 * ```trac_url``` - xmlrpc url to trac, e.g. ``https://user:secret@www.example.com/projects/thisismyproject/login/xmlrpc```

Target
-------

 * ```gitlab_url``` - e.g. ```https://www.exmple.com/gitlab/api/v3```
 * ```gitlab_access_token``` - the access token of the user creating all the issues. Found on the account page,  e.g. ```secretsecretsecret```
 * ```dest_project_name``` - the destination project including the paths to it. Basically the rest of the clone url minus the ".git". E.g. ```jens.neuhalfen/task-ninja```.
 * ```milestone_map``` - Maps milestones from trac to gitlab. Milestones have to exist in gitlab prior to running the script (_CAVE_: Assigning milestones does not work.)
 * ```milestone_list``` - Lists milestones from trac with associated metadata. Manually populated at this point by copy/paste out of trac milestone admin page

License
========

 License: http://www.wtfpl.net/

Requirements
==============

 * ```Python 2.7, xmlrpclib, requests```
 * Trac with xmlrpc plugin enabled
 * Gitlab


Create milestone_list from copy paste admin area trac
==============================================

Copy the milestones from the trac admin page and paste them in your editor of choice that supports regex replace.

Now replace the full text with the following regex and replacement, adjust as you see fit. When done, copy the result in migrate.py.

    regex: \s*([\w\.\s]*?)\s*(\d{2})/(\d{2})/(\d{2})\s[\d:]*\s*(?:(\d{2})/(\d{2})/(\d{2})\s[\d:]*)?\s*\d+
    replace: "$1":{"title":"$1","description":"Trac Import, milestone completed on: 20$7-$5-$6","due_date":"20$4-$2-$3"},\r\n

Create milestone_map from above
----------
Now from the milestone_list you can create a simple map with the following regex and replacement:

    regex: ("[\w\.\s]*"):\{.*\r\n
    replace: $1:$1,
