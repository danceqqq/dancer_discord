# bot.py
import discord
from discord.ext import commands
from config import TOKEN
from verification import verify_user
from slash import setup_slash_commands
import sqlite3
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Создание базы данных и таблицы
conn = sqlite3.connect('nickname_changes.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS changes
             (old_nickname TEXT, new_nickname TEXT, change_time TEXT, discord_id INTEGER)''')
conn.commit()

# Добавление атрибутов db_cursor и db_connection к объекту Bot
bot.db_cursor = c
bot.db_connection = conn

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await setup_slash_commands(bot)

@bot.command()
async def verif(ctx, username: str):
    await verify_user(ctx, username, bot.db_cursor, bot.db_connection)

bot.run(TOKEN)
