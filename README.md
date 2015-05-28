# willie-modules

This is a collection of modules for the [Willie IRC Bot](http://willie.dftba.net/).

(Also available here on [Github](https://github.com/embolalia/willie))


The first implemented module (league.py) is an Info-Plugin for League of Legends.
It's dependent on [RiotWatcher](https://github.com/pseudonym117/Riot-Watcher/).

RiotWatcher is available via `pip install riotwatcher`.




#League

A key for the Riot API is required. Get one here: https://developer.riotgames.com/

## Available commands

- `lstatus` -- Show general status information of League's services
- `sinfo <summoner>` -- Show (as of now) rudimentary info about the summoner
- `sid <summoner` -- Return Summoner ID of given summoner (mostly for debug purposes)
- `wotd <summoner>` -- Shows if and in case it's not, when the next Win of the Day Bonus for the given summoner is available
