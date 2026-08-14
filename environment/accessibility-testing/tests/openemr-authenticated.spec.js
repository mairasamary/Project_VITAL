const { test, expect } = require('@playwright/test');
const fs = require('fs');
const path = require('path');
const { loginOpenEMR } = require('./helpers/openemr-auth');
const { runAxe, compactReport, printSummary } = require('./helpers/axe-report');

const baseURL = process.env.OPENEMR_BASE_URL || 'https://host.docker.internal:8443';
const username = process.env.OPENEMR_ADMIN_USER;
const password = process.env.OPENEMR_ADMIN_PASSWORD;
const patientFinderPath =
  process.env.ACCESSIBILITY_PATIENT_FINDER_PATH ||
  '/interface/main/finder/dynamic_finder.php';

function requireCredentials() {
  if (!username || !password) {
    throw new Error(
      'OPENEMR_ADMIN_USER and OPENEMR_ADMIN_PASSWORD must be supplied via environment variables.'
    );
  }
}

function writeReport(name, report) {
  const outDir = path.resolve(
    __dirname,
    '../../../.project-vital/accessibility-testing/authenticated'
  );
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(
    path.join(outDir, `${name}.json`),
    JSON.stringify(report, null, 2)
  );
}

test.beforeEach(async ({ page }) => {
  requireCredentials();
  await loginOpenEMR(page, baseURL, username, password);
});

test('collect authenticated OpenEMR landing-page accessibility baseline', async ({ page }) => {
  await page.waitForTimeout(1500);

  const results = await runAxe(page);
  const report = compactReport(
    'Authenticated landing page',
    page.url(),
    await page.title(),
    results
  );

  writeReport('authenticated-landing-axe', report);
  printSummary(report);

  // Baseline collection, not zero-violation enforcement.
  expect(report.url).not.toContain('/interface/login/login.php');
});

test('collect patient-finder accessibility baseline', async ({ page }) => {
  const target = new URL(patientFinderPath, baseURL).toString();
  const response = await page.goto(target, {
    waitUntil: 'domcontentloaded',
    timeout: 45_000
  });

  if (!response || !response.ok()) {
    throw new Error(
      `Patient finder target did not load successfully: ${target} ` +
      `(status ${response ? response.status() : 'unknown'})`
    );
  }

  await page.waitForTimeout(1000);

  const results = await runAxe(page);
  const report = compactReport(
    'Patient finder',
    page.url(),
    await page.title(),
    results
  );

  writeReport('patient-finder-axe', report);
  printSummary(report);

  expect(report.url).toContain('finder');
});
