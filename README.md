# MTGTwartBot

Repo to tweet Magic: the Gathering card art alongside the flavour text.

## Installation

Clone and install with pip:

```bash
git clone git@github.com:Tyrannican/twartbot.git

cd twartbot

python -m venv venv

pip install -r requirements.txt

pip install .
```

## Running

Ensure you have the proper Twitter API keys set as the environment variables.

```bash
python -m mtgtwartbot.main
```