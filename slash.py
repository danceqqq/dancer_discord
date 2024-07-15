# slash.py
import discord
from discord import app_commands
from verification import verify_user

async def setup_slash_commands(bot):
    @bot.tree.command(name="verif", description="Введите после команды своё имя, для форматирования имени.")
    async def verif(interaction: discord.Interaction, username: str):
        await verify_user(interaction, username, bot.db_cursor, bot.db_connection)

    await bot.tree.sync()
