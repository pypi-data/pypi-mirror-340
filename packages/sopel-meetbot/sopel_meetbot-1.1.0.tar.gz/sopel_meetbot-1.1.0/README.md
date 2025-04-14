# sopel-meetbot

The `meetbot` plugin formerly shipped with Sopel prior to version 8.0.

_Note: Not super actively maintained. Open an issue if you're interested in
taking over this particular piece of the project!_


## Installation

Place `meetbot.py` into `~/.sopel/plugins/`

## Configuration

```ini
[meetbot]
meeting_log_path = ~/www/meetings
# Path to where the plugin should store meeting logs.
# Intended to be served by a webserver (Apache, Nginx, etc.)

meeting_log_baseurl = https://example.com/~sopel/meetings
# Where the above path can be accessed via HTTP(S)
# (omit trailing slash)
# This will be used to build links to the finished meeting logs.
```

## Special thanks

All contributors to [the original `meetbot` plugin for
Sopel](https://github.com/sopel-irc/sopel/commits/master/sopel/modules/meetbot.py).
