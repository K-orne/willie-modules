import willie.module
import datetime
from riotwatcher.riotwatcher import RiotWatcher
from riotwatcher.riotwatcher import EUROPE_WEST

API_KEY = 'b754af07-6bb2-4745-b26d-bb0a29fd73ed'
w = RiotWatcher(API_KEY, default_region=EUROPE_WEST)


@willie.module.commands('lstatus')
def lstatus(bot, trigger):
    status = w.get_server_status('euw')
    services = status.get('services')
    result = ""
    seq = list()
    for s in services:
        seq.append(s.get('name') + ": " + (s.get('status')))
    result = ' - '.join(seq)
    bot.say('League Status -> '+result)


@willie.module.commands('sinfo')
def sinfo(bot, trigger):
    name = trigger.group(2)
    summoner = w.get_summoner(name)
    result = "Summoner " + summoner['name'] + " is Level " + str(summoner['summonerLevel'])
    bot.say(result)


@willie.module.commands('sid')
def sid(bot, trigger):
    name = w.get_summoner(trigger.group(2))
    result = "Summoner ID for " + name['name'] + " is: " + str(name['id'])
    bot.say(result)


@willie.module.commands('wotd')
def wotd(bot, trigger):
    name = w.get_summoner(trigger.group(2))
    match = w.get_recent_games(name['id'])
    matches = match['games']
    for s in matches:
        if s['stats']['win'] is True:
            recent_match = s
            break

    match_start = recent_match['createDate']
    match_stats = recent_match['stats']
    match_length = match_stats['timePlayed']
    tnow = datetime.datetime.today()
    match_end_timestamp = match_start / 1000.0 + match_length
    last_won_match = datetime.datetime.fromtimestamp(match_end_timestamp)
    timer = datetime.timedelta(hours=22)
    delta = tnow - last_won_match
    if delta > timer:
        bot.say("Last won match for " + name['name'] + " ended on: " + last_won_match.ctime() + ". Win of the day is available.")
    else:
        bot.say("Last won match for " + name['name'] + " ended on: " + last_won_match.ctime() + ". Win of the day is available at " + (last_won_match + timer).strftime("%H:%M:%S"))
