import sys, asyncio, os
from playwright.async_api import async_playwright
root=sys.argv[1]; jobs=[a.split('@') for a in sys.argv[2:]]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        os.makedirs(f"{root}/shots",exist_ok=True)
        for name,w in jobs:
            pg=await b.new_page(viewport={"width":int(w),"height":900})
            await pg.goto(f"file://{os.path.abspath(root)}/local/{name}/preview.html")
            await pg.wait_for_timeout(2500)
            out=f"{root}/shots/{name.replace(' ','_')}_{w}.png"
            await pg.screenshot(path=out,full_page=True); print(out, await pg.evaluate("document.body.scrollHeight"))
        await b.close()
asyncio.run(main())
