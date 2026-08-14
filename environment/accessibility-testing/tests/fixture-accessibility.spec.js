const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;
const path = require('path');

async function scan(page) {
  return await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
    .analyze();
}

test('accessible teaching fixture has no automatically detectable WCAG A/AA violations', async ({ page }) => {
  const fixture = 'file://' + path.resolve(__dirname, '../fixtures/accessible.html');
  await page.goto(fixture);
  const results = await scan(page);
  expect(results.violations).toEqual([]);
});

test('broken teaching fixture is detected by axe', async ({ page }) => {
  const fixture = 'file://' + path.resolve(__dirname, '../fixtures/broken.html');
  await page.goto(fixture);
  const results = await scan(page);

  const ruleIds = results.violations.map(v => v.id);

  // The fixture deliberately contains several common accessibility defects.
  expect(ruleIds.length).toBeGreaterThan(0);
  expect(ruleIds).toContain('label');
  expect(ruleIds).toContain('image-alt');
});
