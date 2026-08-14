const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;
const fs = require('fs');
const path = require('path');

const baseURL = process.env.OPENEMR_BASE_URL || 'https://localhost:9301';

test('scan OpenEMR login page and produce an accessibility baseline', async ({ page }) => {
  await page.goto(baseURL, { waitUntil: 'domcontentloaded' });

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
    .analyze();

  const outDir = path.resolve(__dirname, '../../../.project-vital/accessibility-testing');
  fs.mkdirSync(outDir, { recursive: true });

  const report = {
    url: page.url(),
    title: await page.title(),
    violations: results.violations.map(v => ({
      id: v.id,
      impact: v.impact,
      description: v.description,
      help: v.help,
      helpUrl: v.helpUrl,
      nodes: v.nodes.map(n => ({
        target: n.target,
        html: n.html,
        failureSummary: n.failureSummary,
      })),
    })),
    incomplete: results.incomplete.map(v => ({
      id: v.id,
      impact: v.impact,
      description: v.description,
      help: v.help,
      helpUrl: v.helpUrl,
      nodeCount: v.nodes.length,
    })),
  };

  fs.writeFileSync(
    path.join(outDir, 'openemr-login-axe.json'),
    JSON.stringify(report, null, 2)
  );

  console.log(`OpenEMR login page: ${report.url}`);
  console.log(`Automated violations: ${report.violations.length}`);
  console.log(`Needs manual review/incomplete: ${report.incomplete.length}`);

  for (const v of report.violations) {
    console.log(`  [${v.impact || 'unknown'}] ${v.id}: ${v.help} (${v.nodes.length} node(s))`);
  }

  // Baseline collection: we do NOT require zero violations yet.
  expect(report.url).toContain('http');
});
