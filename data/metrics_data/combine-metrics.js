const fs = require('fs');
const path = require('path');

const metricsDir = 'C:/Users/zbabr/code/SIP/metrics_data';
const files = fs.readdirSync(metricsDir).filter(f => f.endsWith('.json') && f !== 'all-metrics.json' && f !== 'combined-metrics.json');

const combined = {};

files.forEach(file => {
  const repoName = path.basename(file, '.json');
  const filePath = path.join(metricsDir, file);
  const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  combined[repoName] = data;
});

const outputPath = path.join(metricsDir, 'all-metrics.json');
fs.writeFileSync(outputPath, JSON.stringify(combined, null, 2));
console.log(`Combined metrics saved to: ${outputPath}`);
console.log(`Included repositories: ${Object.keys(combined).join(', ')}`);
