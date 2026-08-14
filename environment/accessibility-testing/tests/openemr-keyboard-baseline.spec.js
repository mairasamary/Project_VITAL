const { test, expect } = require('@playwright/test');
const fs = require('fs');
const path = require('path');
const { loginOpenEMR } = require('./helpers/openemr-auth');

const baseURL = process.env.OPENEMR_BASE_URL || 'https://host.docker.internal:8443';
const username = process.env.OPENEMR_ADMIN_USER;
const password = process.env.OPENEMR_ADMIN_PASSWORD;

function labelFor(el) {
  if (!el) return null;
  return (
    el.getAttribute('aria-label') ||
    el.getAttribute('title') ||
    el.innerText ||
    el.getAttribute('name') ||
    el.getAttribute('id') ||
    ''
  ).trim().slice(0, 120);
}

test('collect keyboard focus-sequence evidence on authenticated landing page', async ({ page }) => {
  if (!username || !password) {
    throw new Error('Missing local OpenEMR credentials.');
  }

  await loginOpenEMR(page, baseURL, username, password);
  await page.waitForTimeout(1200);

  const sequence = [];

  for (let i = 0; i < 20; i++) {
    await page.keyboard.press('Tab');

    const item = await page.evaluate(() => {
      const el = document.activeElement;
      if (!el) return null;

      const style = window.getComputedStyle(el);
      const rect = el.getBoundingClientRect();

      const text =
        el.getAttribute('aria-label') ||
        el.getAttribute('title') ||
        el.innerText ||
        el.getAttribute('name') ||
        el.getAttribute('id') ||
        '';

      return {
        tag: el.tagName,
        id: el.id || null,
        name: el.getAttribute('name'),
        role: el.getAttribute('role'),
        accessibleHint: text.trim().slice(0, 120),
        outlineStyle: style.outlineStyle,
        outlineWidth: style.outlineWidth,
        boxShadow: style.boxShadow,
        visible:
          rect.width > 0 &&
          rect.height > 0 &&
          style.visibility !== 'hidden' &&
          style.display !== 'none'
      };
    });

    sequence.push({ tab: i + 1, ...item });
  }

  const outDir = path.resolve(
    __dirname,
    '../../../.project-vital/accessibility-testing/authenticated'
  );
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(
    path.join(outDir, 'keyboard-focus-sequence.json'),
    JSON.stringify(sequence, null, 2)
  );

  console.log('Keyboard focus sequence (first 20 Tab presses):');
  for (const x of sequence) {
    console.log(
      `  ${x.tab}. ${x.tag || 'UNKNOWN'} ` +
      `${x.accessibleHint || '(no accessible hint)'} ` +
      `[outline=${x.outlineStyle}/${x.outlineWidth}]`
    );
  }

  // This is evidence collection, not proof of a good focus order.
  expect(sequence.filter(x => x && x.visible).length).toBeGreaterThan(0);
});
