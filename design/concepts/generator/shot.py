import sys, asyncio
from playwright.async_api import async_playwright
jobs=[a.split('@') for a in sys.argv[1:]]  # name@width@theme
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=["--ignore-certificate-errors"])
        for name,w,th in jobs:
            pg=await b.new_page(viewport={"width":int(w),"height":900})
            await pg.goto(f"file://{__import__('os').getcwd()}/local/{name}/preview.html")
            if th=="night": await pg.evaluate("document.documentElement.setAttribute('data-theme','night')")
            await pg.wait_for_timeout(1500)
            out=f"shots/{name.replace(' ','_')}_{w}_{th}.png"
            await pg.screenshot(path=out,full_page=True); print(out, await pg.evaluate("document.body.scrollHeight"))
        await b.close()
asyncio.run(main())
