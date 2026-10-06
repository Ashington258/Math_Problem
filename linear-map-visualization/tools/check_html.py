"""Browser acceptance checks for the generated offline learning pages."""
from pathlib import Path
import numpy as np
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]


def settle(page):
    page.evaluate('() => pending')


def frame(page,index):
    page.locator('#t').evaluate('(el,v)=>{el.value=v;el.dispatchEvent(new Event("input",{bubbles:true}));}',str(index))
    settle(page)
    actual=page.locator('#tvalue').evaluate('(el)=>el.value')
    assert actual==f'{index/40:.2f}',page.evaluate('() => ({slider:slider.value,output:document.getElementById("tvalue").value,stage:document.getElementById("stage").textContent})')


def check_cloud(page):
    snapshot=page.evaluate('''() => ({kind:current.kind,A:current.matrix,
      cloud:plot.data.find(t=>t.meta?.group==='cloud'),
      target:current.figure.frames[40].data[0]})''')
    actual=snapshot['cloud'];expected=snapshot['target']
    for coord in ['x','y','z']:
        if coord in expected:
            np.testing.assert_allclose(actual[coord],expected[coord],atol=1e-10)


def main():
    qa=ROOT/'output'/'qa';qa.mkdir(parents=True,exist_ok=True)
    with sync_playwright() as p:
        browser=None
        for channel in ['chrome','msedge',None]:
            try:
                browser=p.chromium.launch(channel=channel,headless=True)
                break
            except Exception:
                continue
        if browser is None:
            raise RuntimeError('Install Chrome/Edge or run: python -m playwright install chromium')
        context=browser.new_context(viewport=dict(width=1440,height=1180))
        context.set_offline(True)
        for filename in ['r3_to_r2.html','r2_to_r3.html','four_subspaces.html']:
            page=context.new_page()
            errors=[]
            page.on('pageerror',lambda error:errors.append(str(error)))
            page.goto((ROOT/'output'/'html'/filename).as_uri())
            page.evaluate('() => window.ready')
            assert page.locator('#plot .main-svg').count()>0
            page.locator('[data-group="kernel"]').uncheck()
            settle(page)
            assert page.evaluate('() => plot.data.filter(t=>t.meta?.group==="kernel").every(t=>t.visible===false)')
            frame(page,40);check_cloud(page)
            assert page.evaluate('() => plot.data.filter(t=>t.meta?.group==="kernel").every(t=>t.visible===false)')
            page.locator('[data-group="kernel"]').check();settle(page)
            page.locator('[data-group="labels"]').uncheck();settle(page)
            assert page.evaluate('() => plot.data.filter(t=>t.meta?.group==="labels").every(t=>t.visible===false)')
            page.locator('[data-group="labels"]').check();settle(page)
            if filename=='four_subspaces.html':
                for key,dimension in [('square','3 × 3'),('B','3 × 2'),('A','2 × 3')]:
                    page.select_option('#example',key)
                    try:
                        page.wait_for_function('(text)=>document.querySelector("#dimension").textContent.includes(text)',arg=dimension,timeout=10000)
                    except Exception:
                        raise AssertionError((key,errors,page.locator('#dimension').inner_text()))
                    frame(page,40);check_cloud(page)
            if filename!='r2_to_r3.html':
                page.locator('[data-group="fiber"]').check();settle(page)
                assert page.evaluate('() => plot.data.filter(t=>t.meta?.group==="fiber").every(t=>t.visible===true)')
            # Exercise an actual drag in a 3D viewport, then preserve that camera.
            before=page.evaluate('() => JSON.stringify((plot.layout.scene||plot.layout.scene2).camera)')
            x=350 if filename!='r2_to_r3.html' else 1040
            page.mouse.move(x,420);page.mouse.down();page.mouse.move(x+90,460,steps=12);page.mouse.up()
            page.wait_for_timeout(250)
            after=page.evaluate('() => JSON.stringify((plot.layout.scene||plot.layout.scene2).camera)')
            assert before!=after,'3D orbit did not change the camera'
            page.screenshot(path=str(qa/filename.replace('.html','.png')),full_page=True)
            page.click('#reset');settle(page)
            assert page.locator('#tvalue').evaluate('(el)=>el.value')=='0.00'
            page.click('#play')
            page.wait_for_function('Number(document.querySelector("#t").value)>0')
            page.click('#play');settle(page)
            assert page.locator('#play').inner_text()=='播放'
            assert not errors,errors
            print(filename+': PASS (offline, controls, slider, orbit, playback)')
            page.close()
        browser.close()


if __name__=='__main__':
    main()
