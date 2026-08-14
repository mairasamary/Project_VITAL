const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;
const path = require('path');

async function scan(page) {
  return await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22a', 'wcag22aa'])
    .analyze();
}

test('Project VITAL accessibility CI fixture has no automated WCAG A/AA violations', async ({ page }) => {
  const fixture = 'file://' + path.resolve(__dirname, '../fixtures/ci-accessible.html');
  await page.goto(fixture);

  const results = await scan(page);

  if (results.violations.length) {
    console.log('Accessibility violations:');
    for (const v of results.violations) {
      console.log(`  [${v.impact || 'unknown'}] ${v.id}: ${v.help}`);
      for (const n of v.nodes) {
        console.log(`    target=${JSON.stringify(n.target)}`);
        console.log(`    ${n.failureSummary || ''}`);
      }
    }
  }

  expect(results.violations).toEqual([]);
});

test('keyboard focus reaches the search controls in a meaningful order', async ({ page }) => {
  const fixture = 'file://' + path.resolve(__dirname, '../fixtures/ci-accessible.html');
  await page.goto(fixture);

  const sequence = [];
  for (let i = 0; i < 3; i++) {
    await page.keyboard.press('Tab');
    sequence.push(await page.evaluate(() => {
      const el = document.activeElement;
      return {
        tag: el.tagName,
        id: el.id || '',
        text: (el.innerText || '').trim()
      };
    }));
  }

  expect(sequence[0].id).toBe('family-name');
  expect(sequence[1].id).toBe('dob');
  expect(sequence[2].tag).toBe('BUTTON');
  expect(sequence[2].text).toContain('Search');
});
