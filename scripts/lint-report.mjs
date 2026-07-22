import { spawnSync } from "node:child_process";
import { createRequire } from "node:module";
import fs from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const require = createRequire(import.meta.url);
const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const lintConfigDir = path.join(repoRoot, "config", "lint");
const outputPath = path.join(repoRoot, "docs", "lint-results.md");
const eslintEntry = path.join(
  path.dirname(require.resolve("eslint/package.json")),
  "bin",
  "eslint.js"
);

const REPO_TARGETS = {
  alexandria: {
    eslint: [],
    python: ["repos/alexandria/src"],
  },
  wayfinder: {
    eslint: [],
    python: ["repos/wayfinder/backend/app"],
  },
  VeriFi: {
    eslint: ["repos/VeriFi/frontend/src"],
    python: ["repos/VeriFi/backend/retrieval", "repos/VeriFi/backend/src"],
  },
  Lens: {
    eslint: ["repos/Lens/frontend"],
    python: ["repos/Lens/backend/app"],
  },
  SlugSync: {
    eslint: ["repos/SlugSync/supabase/functions"],
    python: [],
  },
  CsLife: {
    eslint: [],
    python: [],
    notCovered: true,
  },
};

const EXAMPLE_TARGETS = {
  eslint: ["typescript"],
  python: ["python"],
};

const MAX_SAMPLES = 10;

function resolvePython() {
  const venvPython =
    process.platform === "win32"
      ? path.join(repoRoot, ".venv", "Scripts", "python.exe")
      : path.join(repoRoot, ".venv", "bin", "python");

  if (fs.existsSync(venvPython)) {
    return venvPython;
  }

  return process.platform === "win32" ? "python" : "python3";
}

function runCapture(command, commandArgs) {
  return spawnSync(command, commandArgs, {
    cwd: repoRoot,
    encoding: "utf8",
    maxBuffer: 50 * 1024 * 1024,
  });
}

function gitValue(args) {
  const result = runCapture("git", args);
  if (result.status !== 0) {
    return "unknown";
  }
  return result.stdout.trim() || "unknown";
}

function existingPaths(paths) {
  const found = [];
  const missing = [];

  for (const target of paths) {
    const absolute = path.join(repoRoot, target);
    if (fs.existsSync(absolute)) {
      found.push(target);
    } else {
      missing.push(target);
    }
  }

  return { found, missing };
}

function runEslint(paths) {
  if (paths.length === 0) {
    return { status: "na", errors: 0, warnings: 0, samples: [], missing: [] };
  }

  const { found, missing } = existingPaths(paths);
  if (found.length === 0) {
    return {
      status: "missing",
      errors: 0,
      warnings: 0,
      samples: [],
      missing,
    };
  }

  const result = runCapture(process.execPath, [
    eslintEntry,
    "-c",
    path.join(lintConfigDir, "eslint.config.js"),
    "--format",
    "json",
    ...found,
  ]);

  if (result.error) {
    return {
      status: "error",
      errors: 0,
      warnings: 0,
      samples: [result.error.message],
      missing,
    };
  }

  let errors = 0;
  let warnings = 0;
  const samples = [];

  try {
    const reports = JSON.parse(result.stdout || "[]");
    for (const file of reports) {
      errors += file.errorCount ?? 0;
      warnings += file.warningCount ?? 0;
      for (const message of file.messages ?? []) {
        if (samples.length >= MAX_SAMPLES) {
          break;
        }
        const severity = message.severity === 2 ? "error" : "warning";
        samples.push(
          `${file.filePath}:${message.line}:${message.column} ${severity} ${message.message} (${message.ruleId ?? "unknown"})`
        );
      }
    }
  } catch {
    const output = (result.stderr || result.stdout || "").trim();
    return {
      status: "error",
      errors: 0,
      warnings: 0,
      samples: output ? [output.split("\n")[0]] : ["Failed to parse ESLint JSON output"],
      missing,
    };
  }

  const passed = (result.status ?? 1) === 0;
  return {
    status: passed ? "pass" : "fail",
    errors,
    warnings,
    samples,
    missing,
  };
}

function runPylint(paths) {
  if (paths.length === 0) {
    return { status: "na", issues: 0, score: null, samples: [], missing: [] };
  }

  const { found, missing } = existingPaths(paths);
  if (found.length === 0) {
    return {
      status: "missing",
      issues: 0,
      score: null,
      samples: [],
      missing,
    };
  }

  const result = runCapture(resolvePython(), [
    "-m",
    "pylint",
    "--rcfile",
    path.join(lintConfigDir, "pylintrc"),
    ...found,
  ]);

  if (result.error) {
    return {
      status: "error",
      issues: 0,
      score: null,
      samples: [result.error.message],
      missing,
    };
  }

  const output = `${result.stdout ?? ""}\n${result.stderr ?? ""}`.trim();
  const lines = output ? output.split("\n") : [];
  const scoreMatch = output.match(/rated at ([\d.-]+)\/10/);
  const score = scoreMatch ? scoreMatch[1] : null;

  const issueLines = lines.filter(
    (line) =>
      line.includes(": ") &&
      (line.match(/^[A-Z]\d{4}:/) || line.match(/:\d+:\d+:/))
  );

  const samples = issueLines.slice(0, MAX_SAMPLES).map((line) => line.trim());
  const passed = (result.status ?? 1) === 0;

  return {
    status: passed ? "pass" : "fail",
    issues: issueLines.length,
    score,
    samples,
    missing,
  };
}

function runFlake8(paths) {
  if (paths.length === 0) {
    return { status: "na", issues: 0, samples: [], missing: [] };
  }

  const { found, missing } = existingPaths(paths);
  if (found.length === 0) {
    return {
      status: "missing",
      issues: 0,
      samples: [],
      missing,
    };
  }

  const result = runCapture(resolvePython(), [
    "-m",
    "flake8",
    "--config",
    path.join(lintConfigDir, "flake8.ini"),
    ...found,
  ]);

  if (result.error) {
    return {
      status: "error",
      issues: 0,
      samples: [result.error.message],
      missing,
    };
  }

  const lines = (result.stdout ?? "")
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);

  const passed = (result.status ?? 1) === 0;
  return {
    status: passed ? "pass" : "fail",
    issues: lines.length,
    samples: lines.slice(0, MAX_SAMPLES).map((line) => line.trim()),
    missing,
  };
}

function formatToolCell(result, tool) {
  if (result.status === "na") {
    return "N/A";
  }
  if (result.status === "missing") {
    return "Path missing";
  }
  if (result.status === "error") {
    return "Error";
  }

  if (tool === "eslint") {
    const total = result.errors + result.warnings;
    const label = result.status === "pass" ? "Pass" : "Fail";
    return `${total} issue${total === 1 ? "" : "s"} (${label})`;
  }

  if (tool === "pylint") {
    const scoreText = result.score ? `, score ${result.score}/10` : "";
    const label = result.status === "pass" ? "Pass" : "Fail";
    return `${result.issues} issue${result.issues === 1 ? "" : "s"}${scoreText} (${label})`;
  }

  const label = result.status === "pass" ? "Pass" : "Fail";
  return `${result.issues} issue${result.issues === 1 ? "" : "s"} (${label})`;
}

function overallStatus(eslint, pylint, flake8, notCovered) {
  if (notCovered) {
    return "Not covered";
  }

  const results = [eslint, pylint, flake8].filter((r) => r.status !== "na");
  if (results.length === 0) {
    return "Not covered";
  }

  const hasFailure = results.some(
    (r) =>
      r.status === "fail" ||
      r.status === "error" ||
      r.status === "missing"
  );

  return hasFailure ? "Fail" : "Pass";
}

function renderSamples(title, samples) {
  if (samples.length === 0) {
    return `_No issues reported._\n\n`;
  }

  let block = `**Sample ${title}:**\n\n`;
  for (const sample of samples) {
    block += `- \`${sample.replace(/`/g, "'")}\`\n`;
  }
  if (samples.length >= MAX_SAMPLES) {
    block += `- _…truncated (${MAX_SAMPLES} shown)_\n`;
  }
  block += "\n";
  return block;
}

function renderMissingNote(missingLists) {
  const missing = [...new Set(missingLists.flat())];
  if (missing.length === 0) {
    return "";
  }
  return `**Missing paths:** ${missing.map((p) => `\`${p}\``).join(", ")}\n\n`;
}

function renderRepoSection(name, config, results) {
  if (config.notCovered) {
    return `## ${name}\n\nNot covered by centralized lint (no paths in \`scripts/lint.mjs\`).\n\n`;
  }

  let section = `## ${name}\n\n`;

  if (config.eslint.length > 0) {
    section += `**ESLint paths:** ${config.eslint.map((p) => `\`${p}\``).join(", ")}\n\n`;
    section += `- **ESLint:** ${formatToolCell(results.eslint, "eslint")}\n`;
    if (results.eslint.errors > 0 || results.eslint.warnings > 0) {
      section += `  - Errors: ${results.eslint.errors}, Warnings: ${results.eslint.warnings}\n`;
    }
    section += "\n";
  }

  if (config.python.length > 0) {
    section += `**Python paths:** ${config.python.map((p) => `\`${p}\``).join(", ")}\n\n`;
    section += `- **Pylint:** ${formatToolCell(results.pylint, "pylint")}\n`;
    section += `- **Flake8:** ${formatToolCell(results.flake8, "flake8")}\n\n`;
  }

  section += renderMissingNote([
    results.eslint.missing ?? [],
    results.pylint.missing ?? [],
    results.flake8.missing ?? [],
  ]);

  if (config.eslint.length > 0) {
    section += renderSamples("ESLint findings", results.eslint.samples);
  }
  if (config.python.length > 0) {
    section += renderSamples("Pylint findings", results.pylint.samples);
    section += renderSamples("Flake8 findings", results.flake8.samples);
  }

  return section;
}

function buildReport(repoResults, exampleResults) {
  const branch = gitValue(["branch", "--show-current"]);
  const commit = gitValue(["rev-parse", "--short", "HEAD"]);
  const date = new Date().toISOString().slice(0, 10);

  let md = `# Static Analysis Results (Centralized Lint)\n\n`;
  md += `**Generated:** ${date}  \n`;
  md += `**Branch:** ${branch} @ ${commit}  \n`;
  md += `**Regenerate:** \`npm run lint:report\`\n\n`;

  md += `## Notes\n\n`;
  md += `- Pylint \`import-error\` (E0401) is disabled in centralized config — cross-repo runs do not install each repo's Python dependencies.\n`;
  md += `- ESLint uses root \`typescript-eslint\` + \`eslint-plugin-react-hooks\`; repo-specific ESLint configs are not applied.\n`;
  md += `- Flake8 counts are the most directly comparable cross-repo style signal.\n\n`;

  md += `## Summary\n\n`;
  md += `| Repo | ESLint | Pylint | Flake8 | Overall |\n`;
  md += `|------|--------|--------|--------|---------|\n`;

  for (const [name, config] of Object.entries(REPO_TARGETS)) {
    const results = repoResults[name];
    md += `| ${name} | ${formatToolCell(results.eslint, "eslint")} | ${formatToolCell(results.pylint, "pylint")} | ${formatToolCell(results.flake8, "flake8")} | ${results.overall} |\n`;
  }

  const ex = exampleResults;
  md += `| Examples | ${formatToolCell(ex.eslint, "eslint")} | ${formatToolCell(ex.pylint, "pylint")} | ${formatToolCell(ex.flake8, "flake8")} | ${ex.overall} |\n\n`;

  for (const [name, config] of Object.entries(REPO_TARGETS)) {
    md += renderRepoSection(name, config, repoResults[name]);
  }

  md += `## Examples (\`typescript/\`, \`python/\`)\n\n`;
  md += `**ESLint paths:** \`typescript\`\n\n`;
  md += `- **ESLint:** ${formatToolCell(exampleResults.eslint, "eslint")}\n\n`;
  md += `**Python paths:** \`python\`\n\n`;
  md += `- **Pylint:** ${formatToolCell(exampleResults.pylint, "pylint")}\n`;
  md += `- **Flake8:** ${formatToolCell(exampleResults.flake8, "flake8")}\n\n`;
  md += renderSamples("ESLint findings", exampleResults.eslint.samples);
  md += renderSamples("Pylint findings", exampleResults.pylint.samples);
  md += renderSamples("Flake8 findings", exampleResults.flake8.samples);

  return md;
}

const repoResults = {};

for (const [name, config] of Object.entries(REPO_TARGETS)) {
  const eslint = runEslint(config.eslint);
  const pylint = runPylint(config.python);
  const flake8 = runFlake8(config.python);

  repoResults[name] = {
    eslint,
    pylint,
    flake8,
    overall: overallStatus(eslint, pylint, flake8, config.notCovered),
  };
}

const exampleEslint = runEslint(EXAMPLE_TARGETS.eslint);
const examplePylint = runPylint(EXAMPLE_TARGETS.python);
const exampleFlake8 = runFlake8(EXAMPLE_TARGETS.python);

const exampleResults = {
  eslint: exampleEslint,
  pylint: examplePylint,
  flake8: exampleFlake8,
  overall: overallStatus(exampleEslint, examplePylint, exampleFlake8, false),
};

const markdown = buildReport(repoResults, exampleResults);

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, markdown, "utf8");

console.log(`Wrote ${path.relative(repoRoot, outputPath)}`);
