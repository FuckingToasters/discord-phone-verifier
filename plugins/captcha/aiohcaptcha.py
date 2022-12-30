from async_hcaptcha import AioHcaptcha # pip install async-hcaptcha
from plugins.configuration.load import config
_, _, SITEKEY, _, _, _, _, _, _, _, _, _, _ = config().loadconfig()

class Solver:
    async def solution():
        captcha_key = None

        for _ in range(3):
            solver = AioHcaptcha(SITEKEY, "https://discord.com/api/v9/users/@me/phone", {"executable_path": "driver/chromedriver.exe"})
            try:
                captcha_key = await solver.solve(retry_count=5)
                break

            except KeyError: continue
        return captcha_key