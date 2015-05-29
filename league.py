import willie.module
import datetime
from riotwatcher.riotwatcher import RiotWatcher
from riotwatcher.riotwatcher import EUROPE_WEST


def checkConfig(bot):
    if not bot.config.has_option('league', 'api_key') or not bot.config.has_option('league', 'region'):
        return False
    else:
        return [bot.config.league.api_key, bot.config.league.region]


def configure(config):
    """
    | [league] | example     | purpose                                                   |
    | api_key  | 123-456-789 | Grants access to the Riot API                             |
    | region   | EUROPE_WEST | Preselects a region for which to access the API - defunct |
    """
    if config.option('Configure league.py', False):
        config.interactive_add('league', 'api_key', "Riot API-Key")
        config.interactive_add('league', 'region', "Default Region - Check riotwatcher")


# Available regions:
regions = {
    BRAZIL              = 'br',
    EUROPE_NORDIC_EAST  = 'eune',
    EUROPE_WEST         = 'euw',
    KOREA               = 'kr',
    LATIN_AMERICA_NORTH = 'lan',
    LATIN_AMERICA_SOUTH = 'las',
    NORTH_AMERICA       = 'na',
    OCEANIA             = 'oce',
    RUSSIA              = 'ru',
    TURKEY              = 'tr'
    }



@willie.module.commands('lregions')
def lregions(bot):
    bot.reply("Available regions are:" +

@willie.module.commands('lstatus')
def lstatus(bot, trigger):
    w = RiotWatcher(bot.config.league.api_key, default_region=trigger.group(2))
    status = w.get_server_status(trigger.group(2))
    services = status.get('services')
    result = ""
    seq = list()
    for s in services:
        seq.append(s.get('name') + ": " + (s.get('status')))
    result = ' - '.join(seq)
    bot.say('League Status -> ' + result + "Config-options: " + bot.config.league.api_key + ", " + bot.config.league.region)


@willie.module.commands('sinfo')
def sinfo(bot, trigger):
    name = trigger.group(2)
    if bot.config.league.region == "EUROPE_WEST":
        region = EUROPE_WEST
    w = RiotWatcher(bot.config.league.api_key, default_region=region)
    summoner = w.get_summoner(name)
    result = "Summoner " + summoner['name'] + " is Level " + str(summoner['summonerLevel'])
    bot.say(result)


@willie.module.commands('sid')
def sid(bot, trigger):
    w = RiotWatcher(bot.config.league.api_key, default_region=EUROPE_WEST)
    name = w.get_summoner(trigger.group(2))
    result = "Summoner ID for " + name['name'] + " is: " + str(name['id'])
    bot.say(result)


@willie.module.commands('wotd')
def wotd(bot, trigger):
    w = RiotWatcher(bot.config.league.api_key, default_region=EUROPE_WEST)
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
        bot.say("Last won match for " + name['name'] + " ended on: " + last_won_match.ctime() + ". Win of the day is available at " + (last_won_match + timer).strftime("%d.%m - %H:%M:%S"))
