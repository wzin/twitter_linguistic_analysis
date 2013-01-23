# -*- coding: utf-8 -*-

import twitter
from collections import Counter
from inspect import getmembers
import ConfigParser
from twitter_debug import dprint
from translation import pl_to_ang

config = ConfigParser.RawConfigParser()
config.read('lab.cfg')

try:
    global DEBUG
    DEBUG=config.get('global','debug')
    per_user_depth=config.get('global','debug')
    words_count=config.get('global','words_count')
except ConfigParser.NoOptionError, ex:
    print "Could not parse options because %s" % (ex)


try:
    api = twitter.Api(consumer_key=config.get('twitter','consumer_key'),
                  consumer_secret=config.get('twitter','consumer_secret'),
                  access_token_key=config.get('twitter','access_token_key'),
                  access_token_secret=config.get('twitter','access_token_secret'))
except ConfigParser.NoOptionError, ex:
    print "Could not parse config options for twitter because %s" % ex
    raise

group_a = config.get('group_a','members').split(',')
group_b = config.get('group_b','members').split(',')


def count_words(group,twitter_group_name):
    word_list = list()
    statuses = list()
    for nickname in group:
        try :
            timeline_objects = api.GetUserTimeline(nickname,count=per_user_depth)
        except UnicodeEncodeError:
            print "Could not get timeline for %s" % nickname
        except twitter.TwitterError, ex:
            print "Could not get timelines because %s" % ex
            raise
        for status in timeline_objects:
            status_text = pl_to_ang(status.text)
            statuses.append(status_text)



    dprint("Statuses object is below",DEBUG)
    dprint(getmembers(statuses),DEBUG)
    dprint("And the object itself",DEBUG)
    dprint(statuses,DEBUG)
    dprint("this is word_list",DEBUG)
    dprint(word_list,DEBUG)


    for i in range(0,len(statuses)):
        word = statuses.pop().split()
        word_list = word_list + word

    print "Listing group_a: %s " % twitter_group_name
    words_to_count = (word for word in word_list)
    c = Counter(word_list)
    most_common = c.most_common(150)

    return most_common

right_words = count_words(group_a,"rightists")
left_words = count_words(group_b,"leftists/rest")

right_only_words = [x[0] for  x in right_words]
left_only_words = [x[0] for  x in left_words]

right_difference = set(right_only_words) - set(left_only_words)
left_difference = set(left_only_words) - set(right_only_words)

print "Right characteristic words"
print right_difference

print "Left characteristic words"
print left_difference

print "Note - common words are ommited here"
