import { spawnSync } from "node:child_process";
import { createRequire } from "node:module";
import fs from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const require = createRequire(import.meta.url);
const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const lintConfigDir = path.join(repoRoot, "config", "lint");
const eslintEntry = path.join(
  path.dirname(require.resolve("eslint/package.json")),
  "bin",
  "eslint.js"
);

const TS_TARGETS = [
  "typescript",
  "repos/VeriFi/frontend/src",
  "repos/Lens/frontend",
  "repos/SlugSync/supabase/functions",
  "repos/StudyPet-Plus/src",
];

const PY_TARGETS = [
  "python",
  "repos/alexandria/src",
  "repos/wayfinder/backend/app",
  "repos/VeriFi/backend/retrieval",
  "repos/VeriFi/backend/src",
  "repos/Lens/backend/app",
];

const args = process.argv.slice(2);
const pyOnly = args.includes("--py-only");
const tsOnly = args.includes("--ts-only");

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

function run(label, command, commandArgs, options = {}) {
  const result = spawnSync(command, commandArgs, {
    cwd: repoRoot,
    stdio: "inherit",
    ...options,
  });

  if (result.error) {
    console.error(`${label} failed: ${result.error.message}`);
    process.exit(1);
  }

  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }
}

const python = resolvePython();

if (!pyOnly) {
  run("ESLint", process.execPath, [
    eslintEntry,
    "-c",
    path.join(lintConfigDir, "eslint.config.js"),
    ...TS_TARGETS,
  ]);
}

if (!tsOnly) {
  run("Pylint", python, [
    "-m",
    "pylint",
    "--rcfile",
    path.join(lintConfigDir, "pylintrc"),
    ...PY_TARGETS,
  ]);

  run("Flake8", python, [
    "-m",
    "flake8",
    "--config",
    path.join(lintConfigDir, "flake8.ini"),
    ...PY_TARGETS,
  ]);
}
