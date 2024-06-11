# Changelog

All notable changes will be documented in this file for easy read for developers.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### **Disclaimer**
*This changelog is based on the changelogs collectively regrouped in `db/updatelog.json`,
but not all changes are made after open-sourcing of the bot.
Most updates were also made the same day as another one,
because I didn't know about Semantic Versioning at that time,
and I just added another update to changelog everytime I changed something.
Hope all of that won't get you lost, though.*

## [Unreleased]

v2.2.0, eh

This release is Beta; if you put your updater to recieve Beta updates, you will recieve every code change of this unreleased version (current Github version, based on commits given time to time).

### Added

- Developer functionality: bot auto-update (adding and changing files only, or for now)
- Developer functionality: developer mode (skip any update change or file deletion processes, e.g. `startup.py`)
- Host functionality: main.py auto-restart upon server disconnection (startup only)

### Changed

- Embed colours on Discord: error messages, success messages and info messages now differ within a three-colour palette shown in `main.py`, lines 72 to 74 (exception: some commands)
- Database system: automatically deletes unredeemed keys from user data
- Economy extension: removed any usage of the TeamTheOne coins wallet

### Removed

- TeamTheOne coins wallet from all economy extension commands

### Fixed

- Activity status not loading (for some confusing reason)
- Continuation of the discriminator removal (accidental remains)

## [2.1.0] - 2023-07-07

### Added

- First official open-sourced release
- Keys/codes for in-bot rewards, one time per user, either redeemable by one person only or by everyone until manual removal in `db/users.json` (user and economy database, not in the Github)
- New command `/redeem`: redeems codes and keys available upon entered

### Changed

- Command `/changelog` usage: no longer requires a specific page to be entered, will always show all changelogs in short format upon using command without any other instruction
- Database: Name registering system no longer registers discriminator (Discord's new names change)

### Removed

- Command `/gamble`: against Discord ~~Developers~~ ToS (still available in code)

### Fixed

- `ExtensionAlreadyLoaded unexistant`: Directory-specific fix, no longer returns this error upon startup on official bot localhost
- Command `/daily` usage: showed elapsed time between last daily and now instead of remaining time

## [2.0.0] - 2023-05-16

### Added

- New command `/changelog`: lists changelogs shown here, but in the format they were posted in the usage server
- New command `/shop view`: closed item shop
- New command `/daily` (unsure): economy extension command, daily rewards
- Inventory for everyone, for shop and soon-to-be commands
- Economy system: Database automatically registers you upon using any economy extension commmand

### Changed

- Database revamp (API backwards uncompatible change)

### Deprecated

- Command `/gamble`: against Discord ~~Developers~~ ToS

### Removed

- Command `/clocktimer`: timer keeping freezing after five minutes and never counting back

### Fixed

- Economy system: Database "unregistered" errors were removed
- Database: Inventory and wallets no longer automatically reset

## [1.1.3] - 2023-03-12

### Added

- New command `/gamble`: economy extension command, roll your chance to try and get high

## [1.1.2] - 2023-02-28

### Changed

- Command `/help` functionality: embedded help page and made command hybrid (dynamic slash command and text-line `$` command)

## [1.1.1] - 2023-02-28

### Added

- New command `/give`: economy extension command, can give money to someone else from multiserver wallet

## [1.1.0] - 2023-02-27

### Added

- Error recording for easy report and fix
- ~~20 minutes max uptime without inputs~~ (Replit-hosting update, doesn't apply)

## [1.0.4] - 2023-01-25

### Added

- Error message for `Missing Permissions`: ADMIN commands in DMs and as users

## [1.0.3] - 2023-01-25

### Changed

- Command `/clocktimer` duration: expanded by a second (604,800s)

### Fixed

- Command `/rob` usage: fixed "couldn't rob" situation

## [1.0.2] - 2023-01-22

### Changed

- Command `/clocktimer` duration: expanded to a maximum of ~7 days (604,799s)

### Fixed

- Command `/rob` usage: fixed "couldn't rob" situation

## [1.0.1] - 2023-01-22

### Added

- New command `/rob`: economy extension command, serves to "rob" someone else (steal their money from their multiserver wallet)

### Changed

- Extension reload (`/reload`) improvement: easy reloading through Discord

## [1.0.0] - 2023-01-22

### Added

- New command `/clocktimer`: serves as in-Discord timer (requires 24/7 hosting)

### Changed

- Command organisation and bot improvement (made extensions for easy reloading)

## [0.1.0] - 2022-09-16

Basically the first version of the bot... there wasn't much improvement nor changelog at the time, so I'd be buggered if I remembered any change before that.