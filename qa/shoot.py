import sys, asyncio
from playwright.async_api import async_playwright
async def main(skins):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for s in skins:
            for name, w, h in (('desk', 1440, 900), ('mob', 390, 844)):
                pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
                await pg.goto(f'file:///home/claude/qa/mock-{s}.html'); await pg.wait_for_timeout(400)
                await pg.screenshot(path=f'/home/claude/qa/shot-{s}-{name}.png', full_page=True)
                await pg.close()
        await b.close()
asyncio.run(main(sys.argv[1:]))
