const { chromium } = require('playwright');
const AxeBuilder = require('@axe-core/playwright').default;
const { spawn } = require('node:child_process');
const fs = require('node:fs');
const assert = require('node:assert/strict');

(async () => {
  const server = spawn('python3', ['-m', 'http.server', '4173', '--bind', '127.0.0.1', '--directory', '_site'], { stdio: 'ignore' });
  let browser;
  try {
    let ready = false;
    for (let i = 0; i < 40; i++) {
      try { const r = await fetch('http://127.0.0.1:4173/'); ready = r.ok; } catch {}
      if (ready) break;
      await new Promise(resolve => setTimeout(resolve, 150));
    }
    assert(ready, 'Preview server failed to start');
    browser = await chromium.launch();
    fs.mkdirSync('screenshots', { recursive: true });
    for (const width of [320, 390, 768, 1440]) {
      const context = await browser.newContext({ viewport: { width, height: 900 }, reducedMotion: 'reduce' });
      const page = await context.newPage();
      const failures = [];
      page.on('pageerror', e => failures.push(e.message));
      page.on('response', r => { if (r.status() >= 400) failures.push(r.url()); });
      await page.goto('http://127.0.0.1:4173/', { waitUntil: 'networkidle' });
      for (const img of await page.locator('img').all()) {
        await img.scrollIntoViewIfNeeded();
        await img.evaluate(el => el.decode());
      }
      assert.equal(await page.locator('.research-card').count(), 3);
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'Horizontal overflow at ' + width);
      assert(await page.locator('img').evaluateAll(images => images.every(i => i.complete && i.naturalWidth > 0)), 'Broken image');
      for (const id of ['research', 'publications', 'background', 'contact']) {
        await page.locator('nav a[href="/#' + id + '"]').click();
        assert.equal(new URL(page.url()).hash, '#' + id);
      }
      await page.goto('http://127.0.0.1:4173/', { waitUntil: 'networkidle' });
      await page.keyboard.press('Tab');
      assert.equal(await page.locator(':focus').textContent(), 'Skip to content');
      await page.keyboard.press('Enter');
      assert.equal(await page.locator(':focus').getAttribute('id'), 'main');
      const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
      assert.deepEqual(results.violations.map(v => ({ id: v.id, impact: v.impact, targets: v.nodes.map(n => n.target) })), []);
      await page.screenshot({ path: 'screenshots/home-' + width + '.png', fullPage: true });
      await page.goto('http://127.0.0.1:4173/404.html', { waitUntil: 'networkidle' });
      await page.getByRole('link', { name: 'Return home' }).click();
      assert.equal(new URL(page.url()).pathname, '/');
      assert.deepEqual(failures, []);
      console.log('PASS: ' + width + 'px layout, images, navigation, keyboard access, axe, and 404 recovery');
      await context.close();
    }
  } finally {
    if (browser) await browser.close();
    server.kill();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
