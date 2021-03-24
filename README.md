# marslinspike

An Urbit-Signal bridge.

Does not currently work.

Note that this software is currently under development, and I am not responsible for any loss of confidentiality, availability, or integrity of data resulting from use of this software.

## Milestones

* ~~relay text messages from a Signal DM to an Urbit chat~~ **COMPLETE**
* relay text messages from an Urbit chat to a Signal DM
* ~~relay text messages from a Signal group to an Urbit chat~~ **COMPLETE**
* relay text messages from an Urbit chat to a Signal group
* relay image messages from an Urbit chat to Signal
* ~~relay attachments from Signal to Urbit~~ **COMPLETE**
* provide configuration for displaying of reactions, replies, read receipts, typing notifications from Signal to Urbit
* provide commands for viewing group metadata

## Requirements

* [Quinnat](https://github.com/midsum-salrux/quinnat)
* [Semaphore](https://github.com/lwesterhof/semaphore)
* Boto3
* an already-registered Signal number
* a running instance of [signald](https://gitlab.com/signald/signald) (note: this project uses the Debian package)
* an Urbit identity
* an Urbit-compatible S3 bucket

## Setup

Install signald for Debian via the instructions [here](https://gitlab.com/signald/signald/-/blob/main/docs/install/debian.md).

Link signald with your Signal number via:

`signaldctl account link`

Install Quinnat via `pip`:

`pip3 install quinnat`

Install Semaphore via `pip`:

`pip3 install semaphore-bot`

Install boto3 via `pip`:

`pip3 install boto3`

Set up a group on your Urbit for your bridge to reside in.

Copy `example.ini` to `default.ini`, and modify it as appropriate to meet your needs.

Start the bridge:

`python3 main.py`
