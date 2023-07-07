# @MagicHelper (VKBot)

The application helps moderators on game server project [MagicRust](https://vk.com/magicowrust)  

# Features
* Count moderators checks
* Control of the moderators work
* Find banned and suspected players on server
* Count reports and display players with a lot of reports

# Techology stack
* vkbottle
* aiohttp
* pydantic
* loguru

# Develop 

clone repo

```bash
git clone https://github.com/MagicRustHelper/vk_bot.git
```

configure .env file by [env config](/ENV.md)

Run dev application
```bash
make build-d
```

or copy command from `Makefile`
