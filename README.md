# discord_anime_bot

Discord bot that sends anime pictures

[Invite bot](https://discord.com/api/oauth2/authorize?client_id=885948354759106650&permissions=0&scope=bot)

## Commands

```
  get_categories Shows avaliable categories aliases
    alias: gc
  get_waifu      {category}, {amount}(max 30) Shows anime picture. Default category: waifu
    alias: gw
  help           Shows list of commands
  pog            champ
  uptime         Shows uptime in format dddd:hh:mm:ss
```

## Exapmles

```
>gc
['waifu', 'neko', 'shinobu', 'megumin', 'bully', 'cuddle', 'cry', 'hug', 'awoo', 'kiss', 'lick', 'pat', 'smug', 'bonk', 'yeet', 'blush', 'smile', 'wave', 'highfive', 'handhold', 'nom', 'bite', 'glomp', 'slap', 'kill', 'kick', 'happy', 'wink', 'poke', 'dance', 'cringe']

>gw neko 10

>gw waifu

>gw 
```

## Install your bot instance

1. Make sure python3 is installed.
2. Use `pip install -r requirements.txt` to install
   required libraries for python.
3. Obtain token [here](https://discord.com/developers/applications).
4. Enter token to `bot_token.py`
5. Run `discord_bot.py`

License
-------

discord_anime_bot is free and open-source software licensed under the [Apache 2.0 License](https://github.com/create-go-app/cli/blob/master/LICENSE).
