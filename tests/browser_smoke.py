"""Browser checks and reproducible desktop/mobile captures.

Requires Playwright and Chromium. No dependency is needed to serve the site.
Example: python3 tests/browser_smoke.py --output /tmp/nugecid-review --axe /tmp/axe.min.js
"""
import argparse
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import json
from pathlib import Path
import shutil
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def run(output, axe):
    output.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    origin = f'http://127.0.0.1:{server.server_port}'
    reports = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=shutil.which('chromium'), headless=True, args=['--no-sandbox'])
            for width in [320, 390, 768, 1024, 1440]:
                page = browser.new_page(viewport={'width': width, 'height': 900}, reduced_motion='reduce')
                failures = []
                page.on('pageerror', lambda error: failures.append(str(error)))
                page.on('requestfailed', lambda request: failures.append(request.url + ': ' + str(request.failure)))
                for path in sorted(ROOT.glob('*.html')):
                    response = page.goto(origin + '/' + path.name, wait_until='networkidle')
                    assert response.status == 200, path.name
                    page.evaluate('document.fonts.ready')
                    # Trigger every lazy image before checking images or capturing full-page screenshots.
                    page.evaluate('document.querySelectorAll("img").forEach(img => img.loading = "eager")')
                    page.wait_for_function('Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)')
                    assert page.locator('h1').count() == 1, path.name
                    sizes = page.evaluate('({scroll:document.documentElement.scrollWidth,client:document.documentElement.clientWidth})')
                    assert sizes['scroll'] <= sizes['client'], (path.name, width, sizes)
                    assert not failures, failures
                    violations = []
                    if axe and width in (390, 1440):
                        page.add_script_tag(path=str(axe))
                        result = page.evaluate('async () => await axe.run(document, {runOnly:{type:"tag",values:["wcag2a","wcag2aa","wcag21aa","wcag22aa"]}})')
                        violations = [{'id': v['id'], 'impact': v['impact'], 'nodes': [n['target'] for n in v['nodes']]} for v in result['violations']]
                    reports.append({'page': path.name, 'width': width, 'horizontalOverflow': False, 'violations': violations})
                    if width in (390, 1440):
                        page.screenshot(path=str(output / f'{path.stem}-{width}.png'), full_page=True)
                page.close()

            page = browser.new_page(viewport={'width': 390, 'height': 844})
            page.goto(origin + '/index.html', wait_until='networkidle')
            menu = page.locator('.menu')
            assert not menu.evaluate('(node) => node.open')
            page.locator('.menu__toggle').focus()
            page.keyboard.press('Enter')
            assert menu.evaluate('(node) => node.open')
            assert page.locator('.menu__lista a[href="sobre.html"]').is_visible()
            page.screenshot(path=str(output / 'menu-mobile-open.png'))
            page.locator('.menu__lista a[href="sobre.html"]').click()
            assert page.url.endswith('/sobre.html')
            page.goto(origin + '/index.html')
            page.locator('.system-facts').first.locator('summary').click()
            assert page.locator('.system-facts').first.locator('dl').is_visible()
            page.locator('.book-facts summary').click()
            assert page.locator('.book-facts').get_by_text('978-65-01-06618-9', exact=False).first.is_visible()
            page.locator('.capability-facts').first.locator('summary').click()
            assert page.locator('.capability-facts').first.locator('p').is_visible()
            page.keyboard.press('Control+Home')
            page.locator('.skip-link').focus()
            page.keyboard.press('Enter')
            assert page.url.endswith('#conteudo')
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    (output / 'browser-results.json').write_text(json.dumps(reports, indent=2))
    problems = [r for r in reports if r['violations']]
    print(f'{len(reports)} page/viewport checks; keyboard menu, disclosures and skip link passed; {len(problems)} pages with accessibility violations.')
    if problems:
        print(json.dumps(problems, indent=2))
        raise SystemExit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path('/tmp/nugecid-review'))
    parser.add_argument('--axe', type=Path)
    args = parser.parse_args()
    run(args.output, args.axe)
