# Changelog

All changes will be documented in this file for easy read for developers and most users.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### **Disclaimers**
- *This changelog is based on the changelogs collectively regrouped in `db/updatelog.json`,
but not all changes are made after open-sourcing of the bot.
Most updates were also made the same day as another one,
because I didn't know about Semantic Versioning at that time,
and I just added another update to changelog everytime I changed something.
Hope all of that won't get you lost, though.*
- *The whole bot is still in development - in INDEV alpha precisely - and may have changes to come.*
- ***DO NOT TRY TO PARSE THIS FILE UNLESS YOU'RE SURE**: the file is only BASED and has edits on the version numbers that contain lowercase letters at the end, which may return errors while using a premade parser.*
  - A means Alpha (not INDEV);
  - B means Beta (not INDEV);
  - I means INDEV, regardless of version type;
  - U means *ANY non-released version not able to be classified under A or B*
- If you look for tags of previous releases in [the specified section](#tags), you may not find anything older than v2.1.0i, and for a normal reason: I don't have any backup or version of these old updates.
- Changelogs for v2.1.0i and under were made before the idea of open-sourcing the bot. Some lines may include changed bot behaviour only on the hosted bot code before July 2023.

## [Unreleased]

This release is INDEV / Alpha; if you put your updater to recieve non-released updates, you will recieve every code change of this unreleased version (current Github version, based on commits given time to time).

If you don't know how to do that, just... check the documentation (TBA).

### Added

- Developer functionality: bot auto-update with `update.py` (adding and changing files only, or for now)
  - *Note:* updater available INDEV v2.1.0 to v2.2.0 and higher: check page in documentation (TBA)
- Developer functionality: developer mode (skip any update change or file deletion processes, e.g. `startup.py`, process covered in documentation)
- Host functionality: main.py auto-restart upon missing Internet connection (only on startup)
- New log file: `fulldiscord.log`: registers all events, even DEBUG, to include Discord module action log
- New command log level: `CDEBUG`, for command debug objects (only appears in log files)
- New database: `alldirs.json`: contains all types of file paths (useful for updates)
- New command: `/echo`: the bot says what you want to say (please no random shit in it, I don't have the mood to make a filter for everything in that...)

### Changed

- All updatelog: added INDEV in version numbers; changed beta variables to unreleased
- Embed colours on Discord: error messages, success messages and info messages now differ within a three-colour palette shown in `main.py`, lines 100 to 104 (exception: some commands)
- Database system: automatically deletes unredeemed keys from separate user data (database cleanup system)
- Economy extension: removed any usage of the TeamTheOne coins wallet
- `/ban`: Tries to message banned user before ban, now responds in embeds in same channel (Dyno-alike concept)
  - Can be improved further in future update
- Main log file `discord.log` now supports `CDEBUG`, a command return separate action log (multi-update change)

### Deprecated

- Nothing here, yet... ***only yet...***

### Removed

- Command `/gamble`: full removal from source code
- TeamTheOne coins wallet from all economy extension commands
- Comments at the end of every single line of code (seemed to me like that)

### Fixed

- Activity status not loading (for some confusing reason)
- Continuation of the discriminator removal (accidentally left remains)

## [2.1.0i] - 2023-07-07

### Added

- First official open-sourced release
- Keys/codes for in-bot rewards, one time per user, either redeemable by one person only or by everyone until manual removal in `db/users.json` (user and economy database, not in the Github)
- New command `/redeem`: redeems codes and keys available upon entered

### Changed

- Command `/changelog` usage: no longer requires a specific page to be entered, will always show all changelogs in short format upon using command without any other instruction
- Database: Name registering system no longer registers discriminator (Discord's new names change)

### Deprecated

- TeamTheOne coins wallet (not announced in original update: announced way later)
- "Partner system" Discord-like concept (was never announced, got shadow-removed by lack of usage and development on that system)

### Removed

- Command `/gamble`: can't be run no more (against Discord ~~Developers~~ ToS: Gambling)

### Fixed

- `ExtensionAlreadyLoaded unexistant`: Directory-specific fix, no longer returns this error upon startup on official bot localhost
- Command `/daily` usage: showed elapsed time between last daily and now instead of remaining time

## [2.0.0i] - 2023-05-16

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

## [1.1.3i] - 2023-03-12

### Added

- New command `/gamble`: economy extension command, roll your chance to try and get high

## [1.1.2i] - 2023-02-28

### Changed

- Command `/help` functionality: embedded help page and made command hybrid (dynamic slash command and text-line `$` command)

## [1.1.1i] - 2023-02-28

### Added

- New command `/give`: economy extension command, can give money to someone else from multiserver wallet

## [1.1.0i] - 2023-02-27

### Added

- Error recording for easy report and fix
- ~~20 minutes max uptime without inputs~~ (Replit-hosting update, doesn't apply)

## [1.0.4i] - 2023-01-25

### Added

- Error message for `Missing Permissions`: ADMIN commands in DMs and as users

## [1.0.3i] - 2023-01-25

### Changed

- Command `/clocktimer` duration: expanded by a second (604,800s)

### Fixed

- Command `/rob` usage: fixed "couldn't rob" situation

## [1.0.2i] - 2023-01-22

### Changed

- Command `/clocktimer` duration: expanded to a maximum of ~7 days (604,799s)

### Fixed

- Command `/rob` usage: fixed "couldn't rob" situation

## [1.0.1i] - 2023-01-22

### Added

- New command `/rob`: economy extension command, serves to "rob" someone else (steal their money from their multiserver wallet)

### Changed

- Extension reload (`/reload`) improvement: easy reloading through Discord

## [1.0.0i] - 2023-01-22

### Added

- New command `/clocktimer`: serves as in-Discord timer (requires 24/7 hosting)

### Changed

- Command organisation and bot improvement (made extensions for easy reloading)

## [0.1.0i] - 2022-09-16

First version on the bot, based on the Discord.py official documentation.

## Tags
