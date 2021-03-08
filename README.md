# marslinspike

An Urbit-Signal bridge.

Does not currently work.

Note that this software is currently under development, and I am not responsible for any loss of confidentiality, availability, or integrity of data resulting from use of this software.

## Milestones

[you are here]

* relay text messages from a Signal DM to an Urbit chat
* relay text messages from an Urbit chat to a Signal DM
* relay text messages from a Signal group to an Urbit chat
* relay text messages from an Urbit chat to a Signal group
* relay image messages from an Urbit chat to Signal
* relay image messages from Signal to Urbit
* provide configuration for displaying of reactions, replies, read receipts, typing notifications from Signal to Urbit
* provide commands for viewing group metadata

## Requirements

* [Quinnat](https://github.com/midsum-salrux/quinnat)
* an already-registered Signal number
* a running instance of [signald](https://gitlab.com/signald/signald)
* an Urbit identity

## Setup

Install Quinnat and pysignald-async via `pip`.

Set up a group for your bridge to reside in.

Copy `example.ini` to `default.ini`, and modify it as appropriate to meet your needs.

Start the bridge:

python3 main.py
