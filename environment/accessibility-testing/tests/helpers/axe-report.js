const AxeBuilder = require('@axe-core/playwright').default;

async function runAxe(page) {
  return await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22a', 'wcag22aa'])
    .analyze();
}

function compactReport(pageName, url, title, results) {
  return {
    pageName,
    url,
    title,
    violations: results.violations.map(v => ({
      id: v.id,
      impact: v.impact,
      description: v.description,
      help: v.help,
      helpUrl: v.helpUrl,
      tags: v.tags,
      nodes: v.nodes.map(n => ({
        target: n.target,
        html: n.html,
        failureSummary: n.failureSummary
      }))
    })),
    incomplete: results.incomplete.map(v => ({
      id: v.id,
      impact: v.impact,
      description: v.description,
      help: v.help,
      helpUrl: v.helpUrl,
      tags: v.tags,
      nodeCount: v.nodes.length
    }))
  };
}

function printSummary(report) {
  console.log(`Page: ${report.pageName}`);
  console.log(`URL: ${report.url}`);
  console.log(`Automated violations: ${report.violations.length}`);
  console.log(`Needs manual review/incomplete: ${report.incomplete.length}`);
  for (const v of report.violations) {
    console.log(
      `  [${v.impact || 'unknown'}] ${v.id}: ${v.help} (${v.nodes.length} node(s))`
    );
  }
}

module.exports = { runAxe, compactReport, printSummary };
