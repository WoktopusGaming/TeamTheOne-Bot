# Changelog

All changes will be documented in this file for easy read for developers and most users.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This changelog is not parsed and might not be able to be parsed currently, as it is manually edited.

### **Disclaimers**
- *Changelogs before v2.2.0i/0.1.1 are based on the changelogs collectively regrouped in `db/updatelog.json`,
but not all changes are made after open-sourcing of the bot.
Most updates were also made the same day as another one,
because I didn't know about Semantic Versioning at that time,
and I just added another update to changelog everytime I changed something.
Hope all of that won't get you lost, though.*
- Changelogs for 2.1.0i/0.1.0 and under were made before the idea of open-sourcing the bot whilst in local development.
Some lines may include workarounds only on the official side of the bot before its localhosting period,
which started on May 2023 by previous host backup, and before its open-sourcing on July 2023.
- *The whole bot is still in development - in alpha precisely - and may have a lot of changes to come.*
- ***DO NOT TRY TO PARSE THIS FILE UNLESS YOU'RE SURE***:
the file has one or more versions portrayed by the lowercase letter I after it's version.
Those are versions made during the INDEV phase of the bot, when it was hosted on repl.it.
Newer versions will be accounted without the lowercase letter.
- If you look for tags of previous releases,
you may not find anything older than 2.1i/0.1.0, and for a normal reason:
source code does not have any version of those old updates. A backup of the first version exists currently for the 
- TAKE NOTE OF THE FOLLOWING:
  - The updater file will recieve more updates post 2.1i/0.1 for optimisation and make it auto-reliable on itself.
  - The startup file is subject to a change soon or later.
  - This whole changelog is subject to a change sooner or later due to a new parsing system I want to develop for the bot.
  It will so then exclude all versions prior to 2.0i/0.0,
  which will be considered the first development "release",
  and 2.1i/0.1 the first open-source release.
  Commit timeline doesn't go any further than 2.1i/0.1 anyways.
  - Disclaimers will soon disappear from changelog to parse more easily. So will most text.
  - The update numbers are *subject to change at any time in the near future.*

## [Unreleased]
Also known as version 0.1.1, formerly known as version 2.2.0i.

### Added

- Developer functionality: bot auto-update with `update.py` (adding and changing files only, or for now)
  - *Note:* updater available 2.1.0i/0.1.0 and under to 2.2.0i/0.1.1 and higher: check page in documentation (TBD)
- Developer functionality: developer mode (skip any update change or file deletion processes, e.g. `startup.py`, process covered in documentation)
- Local host / auto run functionality: `update.py` now support command line arguments `--upgrade` and `--install` for faster invoking of these processes
- Local host / auto run functionality: `main.py` now supports command line argument `--devmode` for enabling developer mode faster than database check
- Host functionality: main.py auto-restart upon missing Internet connection (only on startup)
- New log file: `fulldiscord.log`: registers all events, even DEBUG, to include Discord module action log
- New command log level: `CDEBUG`, for command debug objects (only appears in log files to not overload terminal)
- New database: `alldirs.json`: contains all types of file paths (necessary for updates)
- New command: `/echo`: the bot says what you want to say (please no random shit in it, I don't have the mood to make a filter for everything in that...)
- New command group: `/shop`: this will be the future shop command group. (In works as this commit's date is released.)

### Changed

- Changelog now only mention code changes, and not official bot-only changes
- All updatelog: added INDEV in version numbers; changed beta variables to unreleased
- Embed colours on Discord: error messages, success messages and info messages now differ
- Database system: automatically deletes unredeemed keys from separate user data (database cleanup system)
  - Only useful if host used v2.1.0i or older systems
- `/ban`: Tries to message banned user before ban, now responds in embeds in same channel (Dyno-alike concept)
  - Can be improved further in the future
- Main log file `discord.log` now supports `CDEBUG`, a command return separate action log (multi-update change)
- Some functions (server specific or exclusive to the official bot) were added
  - Some inventory, buffs and wheel functions are official to the bot, yes (due to database structure) even though they ain't added in this version
- Switched to edited WTFPL license

### Deprecated

- All updates before v2.0.0i in the updatelog will be removed later for irrelevance with the current bot (I am breaking the bot's history, yes)
  - They are kept in this changelog here, but will be in a "older changelog" section
  - All changelogs that were replaced from the old system will have a "formerly" statement underneath their header
- Updater: auto-updating the updater will be deprecated from main.py as updater will auto-update itself before all-dirs
  - (Only applies for all users who have used the Beta v2.2i version of the bot; if not used, this doesn't apply to you)
  - This is a possible deprecation; it might not happen at all
- Changelogs: This Markdown file will soon be required to be on all directories due to parsing (I am replacing updatelog.json)
- ***All version numbers are deprecated and soon to be replaced - this might require a manual reinstall of the updatelog (I'll try to not require it)***

### Removed

- Command `/gamble`: full removal from source code
- TeamTheOne coins wallet from all economy extension commands
- Comments at the end of every single line of code (seemed to me like that)

### Fixed

- Activity status not loading (for some confusing reason)
- Official bot: Continuation of the discriminator removal (accidentally left remains)
- Other bug fixes here and there (bugs I found very late)

## [0.1.0] - 2023-07-07
Formerly known as version 2.1.0i.

### Added

- First official open-sourced release (GPL-3.0 license)
- Keys/codes for in-bot rewards, one time per user, either redeemable by one person only or by everyone until manual removal in `db/users.json` (user and economy database, not in the Github)
- New command `/redeem`: redeems codes and keys available upon entered

### Changed

- Command `/changelog` usage: no longer requires a specific page to be entered, will always show all changelogs in short format upon using command without any other instruction
- Database: Name registering system no longer registers discriminator (Discord's new names change)

### Deprecated

- TeamTheOne coins wallet (not announced in original update: announced way later)
- "Partner system" Discord-like concept (was never announced, got shadow-removed three days after update by lack of usage and development on that system)

### Removed

- Command `/gamble`: can't be run no more (against Discord ~~Developers~~ ToS: Gambling)

### Fixed

- `ExtensionAlreadyLoaded unexistant`: Directory-specific fix, no longer returns this error upon startup on official bot localhost
- Command `/daily` usage: showed elapsed time between last daily and now instead of remaining time

## 0.0.0 - 2023-05-16
Formerly known as version 2.0.0i;
also known as initial commit version.

All changes written under are changes made in comparison to older versions.

### Added

- New command `/changelog`: lists changelogs shown here, but in the format they were posted in the usage server
- New command `/shop view`: closed item shop
- New command `/daily` (unsure): economy extension command, daily rewards
- Inventory for everyone, for shop and soon-to-be commands
- Economy system: Database automatically registers you upon using any economy extension commmand
- "Partner system" Discord-like concept (unused but announced in updatelog)

### Changed

- Database revamp (API backwards uncompatible change)

### Deprecated

- Command `/gamble`: against Discord ~~Developers~~ ToS

### Removed

- Command `/clocktimer`: timer keeping freezing after five minutes and never counting back
- Embedded hybrid help page (too much errors for handling at that time) - temporary removal

### Fixed

- Economy system: Database "unregistered" errors were removed
- Database: Inventory and wallets no longer automatically reset

# Old Changelog

## 1.1.3i - 2023-03-12

### Added

- New command `/gamble`: economy extension command, roll your chance to try and get high

### Removed

- Embedded `/help` command: it is now only hybrid

## 1.1.2i - 2023-02-28

### Changed

- Command `/help` functionality: embedded help page and made command hybrid (dynamic slash command and text-line `$` command)

## 1.1.1i - 2023-02-28

### Added

- New command `/give`: economy extension command, can give money to someone else from multiserver wallet

## 1.1.0i - 2023-02-27

### Added

- Error recording for easy report and fix
- ~~20 minutes max uptime without inputs~~ (Replit-hosting update, doesn't apply)

## 1.0.4i - 2023-01-25

### Added

- Error message for `Missing Permissions`: ADMIN commands in DMs and as users

## 1.0.3i - 2023-01-25

### Changed

- Command `/clocktimer` duration: expanded by a second (604,800s)

### Fixed

- Command `/rob` usage: fixed "couldn't rob" situation

## 1.0.2i - 2023-01-22

### Changed

- Command `/clocktimer` duration: expanded to a maximum of ~7 days (604,799s)

### Fixed

- Command `/rob` usage: fixed "couldn't rob" situation

## 1.0.1i - 2023-01-22

### Added

- New command `/rob`: economy extension command, serves to "rob" someone else (steal their money from their multiserver wallet)

### Changed

- Extension reload (`/reload`) improvement: easy reloading through Discord

## 1.0.0i - 2023-01-22

### Added

- New command `/clocktimer`: serves as in-Discord timer (requires 24/7 hosting)

### Changed

- Command organisation and bot improvement (made extensions for easy reloading)

## 0.0.0i - 2022-09-16

First version on the bot, based on the Discord.py official documentation (Replit's auto configuration)

[UNRELEASED]: https://github.com/WoktopusGaming/TeamTheOne-Bot/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/WoktopusGaming/TeamTheOne-Bot/releases/tag/v0.1.0