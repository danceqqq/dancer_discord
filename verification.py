# verification.py
import discord
from datetime import datetime


async def verify_user(ctx, username: str, cursor, connection):
    user = ctx.author if hasattr(ctx, 'author') else ctx.user
    old_nickname = user.display_name
    new_nickname = f'【 {username} 】 {user.name}'
    await user.edit(nick=new_nickname)

    # Запись изменения в базу данных
    change_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO changes (old_nickname, new_nickname, change_time, discord_id) VALUES (?, ?, ?, ?)',
                   (old_nickname, new_nickname, change_time, user.id))
    connection.commit()

    if hasattr(ctx, 'send'):
        await ctx.send(f'Готово! Теперь ваше имя на сервере {new_nickname}')
    else:
        await ctx.response.send_message(f'Готово! Теперь ваше имя на сервере {new_nickname}')
