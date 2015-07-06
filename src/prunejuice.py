import praw
import urllib

usr = raw_input('Username: ')
pwd = raw_input('Password: ')

print 'Running script...'
reddit = praw.Reddit(user_agent='prunejuice')

print 'Logging in...'
reddit.login(usr, pwd)

print 'Fetching saved submissions...'
saved = reddit.user.get_saved(limit=None)

print 'Processing submissions...'
dead_links = 0
duplicate_author_links = 0
author_set = set()
for sub in saved:
    """ Remove dead links"""
    try:
        resp = urllib.urlopen(sub.url)
        if 400 <= resp.getcode() < 500:
            print 'Unsaving \"{0}\" for dead link...'.format(sub.title)
            sub.unsave()
            dead_links += 1
            continue
    except IOError:
        # todo: verify dead/retry
        print 'Unable to resolve submission status...'

    """ Remove duplicate author links """
    if sub.author is not None:
        if sub.author.name in author_set:
            print 'Unsaving \"{0}\" for duplicate author \"{1}\"...'.format(sub.title, sub.author.name)
            sub.unsave()
            duplicate_author_links += 1
            continue
        else:
            author_set.add(sub.author.name)

print 'Done.'
print
print 'Results'
print '----------'
print 'Unsaved dead links: {0}'.format(dead_links)
print 'Unsaved duplicate author links: {0}'.format(duplicate_author_links)
print
