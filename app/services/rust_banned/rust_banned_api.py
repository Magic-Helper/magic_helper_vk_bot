import aiohttp

from app.core import constants, settings
from app.services.rust_banned.models import RustBannedResponse

API_LINK = 'https://rustbanned.com/api/eac_ban_check_v2.php'


async def get_eac_info(steamid: int) -> RustBannedResponse:
    params = _get_eac_info_params(steamid)
    data = await _get_json(API_LINK, params=params)
    response = data['response'][0]
    return RustBannedResponse(**response)


def _get_eac_info_params(steamid: int) -> dict:
    return {
        'apikey': settings.RUST_BANNED_API_KEY,
        'steamid64': steamid,
    }


async def _get_json(url: str, params: dict) -> dict:
    session_headers = _get_session_headers()
    async with aiohttp.ClientSession(headers=session_headers) as session:
        async with session.get(url=url, params=params) as response:
            return await response.json(content_type='application/json')


def _get_session_headers() -> dict:
    return {'User-Agent': constants.USER_AGENT}
