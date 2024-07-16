import requests
from discord.ext import commands
import re

# Функция для извлечения Steam ID из URL
def extract_steam_id(url):
    match = re.search(r'/id/(\w+)', url)
    if match:
        custom_id = match.group(1)
        try:
            response = requests.get(f'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key=ВАШ_API_KEY&vanityurl={custom_id}')
            if response.status_code == 403:
                print('Access denied. Please verify your API key.')
                return None
            data = response.json()
            if data['response']['success'] == 1:
                return data['response']['steamid']
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(f'Error fetching Steam ID: {e}')
            return None
        except ValueError as e:
            print(f'Error decoding JSON: {e}')
            return None
    match = re.search(r'/profiles/(\d+)', url)
    if match:
        return match.group(1)
    return None

# Функция для получения статистики игрока из OpenDota API
def get_player_stats(steam_id):
    try:
        response = requests.get(f'https://api.opendota.com/api/players/{steam_id}')
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print('Player not found in OpenDota database.')
            return None
        else:
            print('Error fetching player stats.')
            return None
    except requests.exceptions.RequestException as e:
        print(f'Error fetching player stats: {e}')
        return None

# Команда для получения статистики игрока
@commands.command(name='dotastat')
async def dota_stat(ctx, steam_url: str):
    steam_id = extract_steam_id(steam_url)
    if not steam_id:
        await ctx.send('Неверная ссылка на Steam аккаунт. Пожалуйста, используйте формат: /dotastat https://steamcommunity.com/id/ваш_ид или /dotastat https://steamcommunity.com/profiles/ваш_ид')
        return

    stats = get_player_stats(steam_id)
    if not stats:
        await ctx.send('Не удалось получить статистику. Пожалуйста, попробуйте позже или убедитесь, что аккаунт связан с OpenDota.')
        return

    profile = stats.get('profile', {})
    mmr_estimate = stats.get('mmr_estimate', {}).get('estimate', 'N/A')
    rank_tier = stats.get('rank_tier', 'N/A')

    response = (
        f"**Статистика игрока Dota 2**\n"
        f"**Имя:** {profile.get('personaname', 'N/A')}\n"
        f"**MMR:** {mmr_estimate}\n"
        f"**Ранг:** {rank_tier}\n"
        f"**Профиль:** {profile.get('profileurl', 'N/A')}\n"
    )

    await ctx.send(response)
