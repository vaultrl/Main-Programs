Bot was built with Python 3 and is running on a AWS EC2 Ubuntu instance. 
Requires discord fuzzywuzzy and python-levenshtein to work
If you use the Dockerfile included it will preinstall everything needed.
    - Use with docker on any major linux distro.

Bot Has a Customizable prefix

Bot Has These Main Features:

Change Nicknames
  - Users can submit a new nickname to be applied to themselves.
    - Use the Nick command

Report Users
  - Users can report another misbehaving user.
  - Upon accepting the report the offending user will be muted.    
    - Use the Report command

Chat Filter
  - Removes words and links from a predefined list
    - Can change values in list
    - Can handle every type of link.
    - The list in the code is very vulgar. Fair warning before looking at it
    - Currently allows to remove blacklists.

Admin Logging
  - Logs deleted messages and files

Test Discord (Invite only has 25 uses): https://discord.gg/yy8ycZwP5k