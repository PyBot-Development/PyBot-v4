from discord.ext import commands
import os
from colorama import *
from resources import checks, support

prefix=support.config.get("prefix")
bot=commands.Bot(command_prefix=commands.when_mentioned_or(prefix), case_insensitive=True)
bot.remove_command('help')
bot.add_check(checks.log())

print(f"{Fore.LIGHTYELLOW_EX}Loading cogs... {Fore.LIGHTGREEN_EX}Please wait{Style.RESET_ALL}")
cogscount = 0
for filename in os.listdir(f'{support.path}/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        cogscount += 1
        if support.config.get("debug"):
            print(f'{Fore.LIGHTCYAN_EX}Loaded extension{Style.RESET_ALL}: {Fore.LIGHTGREEN_EX}{filename[:-3]}{Style.RESET_ALL}')
print(f"{Fore.LIGHTYELLOW_EX}Loading done, Cogs count: {Fore.LIGHTGREEN_EX}{cogscount} {Style.RESET_ALL}")
bot.remove_command('purge')
with open(f"logs/{support.startup_date}.log", "a+") as file:
    file.write(f"{support.startup_date}: [STARTUP] Bot is running!\n")

def bot_run():
    print(f"{Fore.LIGHTMAGENTA_EX}Welcome! Bot is online{Style.RESET_ALL}")
    bot.run(support.config.get("token"), bot=not support.config.get("self-bot"))
    print(f'{Fore.LIGHTRED_EX}Something Failed.')

if __name__ == "__main__":
    bot_run()