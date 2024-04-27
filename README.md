# nextcloud-status
A command line utility to set your nextcloud status and status message.

## Installation

`pip install nextcloud-status`

or 

`pip install https://github.com/coljac/nextcloud-status`

for the latest version if it's not on PyPi.

## Usage

The first time you run, it will prompt you for your NextCloud url, username and password. I recommend making an app-specific password: [See](https://help.nextcloud.com/t/where-to-create-app-password/157454). Config will be in `~/.config/nextcloud-status` on unix or in `AppData/Local` on Windows.

For help:

!(Help)[docs/help.gif]

Or for sub-commands:

!(Help subcommand)[docs/help-sub.gif]

To set the status and message:

!(Set status)[docs/set.gif]

To use an emoji:

!(Emoji)[docs/set-emoji.gif]

To use github markup:

!(Emoji github)[docs/set-gh.gif]

Please create an issue with any bugs.