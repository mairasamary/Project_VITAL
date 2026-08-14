const { expect } = require('@playwright/test');

async function firstVisible(page, selectors) {
  for (const selector of selectors) {
    const loc = page.locator(selector).first();
    if (await loc.count() && await loc.isVisible().catch(() => false)) {
      return loc;
    }
  }
  return null;
}

async function loginOpenEMR(page, baseURL, username, password) {
  await page.goto(baseURL, { waitUntil: 'domcontentloaded', timeout: 45_000 });

  const user = await firstVisible(page, [
    'input[name="authUser"]',
    '#authUser',
    'input[autocomplete="username"]',
    'input[type="text"]'
  ]);

  const pass = await firstVisible(page, [
    'input[name="clearPass"]',
    '#clearPass',
    'input[autocomplete="current-password"]',
    'input[type="password"]'
  ]);

  if (!user || !pass) {
    const inputs = await page.locator('input, select, button').evaluateAll(nodes =>
      nodes.map(n => ({
        tag: n.tagName,
        id: n.id,
        name: n.getAttribute('name'),
        type: n.getAttribute('type'),
        ariaLabel: n.getAttribute('aria-label')
      }))
    );
    throw new Error(
      'Could not identify OpenEMR login controls. Controls found: ' +
      JSON.stringify(inputs)
    );
  }

  await user.fill(username);
  await pass.fill(password);

  const submit = await firstVisible(page, [
    'button[type="submit"]',
    'input[type="submit"]',
    'button:has-text("Login")',
    'button:has-text("Log In")'
  ]);

  if (!submit) {
    throw new Error('Could not identify OpenEMR login submit control.');
  }

  await Promise.all([
    page.waitForLoadState('domcontentloaded').catch(() => {}),
    submit.click()
  ]);

  // OpenEMR can transition through several authenticated URLs/frames.
  await page.waitForTimeout(2500);

  const url = page.url();
  if (url.includes('/interface/login/login.php')) {
    const visibleText = await page.locator('body').innerText().catch(() => '');
    throw new Error(
      'Login appears to have remained on the login page. ' +
      'Check the local semester credentials. Visible page text begins: ' +
      visibleText.slice(0, 500)
    );
  }

  expect(url).toContain('http');
  return url;
}

module.exports = { loginOpenEMR };
