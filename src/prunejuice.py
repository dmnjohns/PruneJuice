import praw
import urllib

user = raw_input('Username: ')
passwd = raw_input('Password: ')

print 'Running script...'
reddit = praw.Reddit(user_agent='prunejuice')

print 'Logging in...'
reddit.login(user, passwd)

print 'Fetching saved submissions...'
saved = reddit.user.get_saved(limit=None)

print 'Checking submissions for dead links...'\
for sub in saved:
    timedout = False
    try:
        resp = urllib.urlopen(sub.url)
    except IOError:
        timedout = True
    if resp.getcode() == 404 or timedout:
        sub.unsave()
        print 'Unsaving \"' + sub.title + '\"...'

print 'Done.'