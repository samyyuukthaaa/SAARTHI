import { spawn, execSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..");
const backendDir = path.join(rootDir, "backend");

// Terminal colors
const cyan = (text) => `\x1b[36m${text}\x1b[0m`;
const green = (text) => `\x1b[32m${text}\x1b[0m`;
const yellow = (text) => `\x1b[33m${text}\x1b[0m`;
const bold = (text) => `\x1b[1m${text}\x1b[0m`;

console.log(bold("=================================================="));
console.log(bold(" 🚀 Saarathi — Full-Stack Development Environment"));
console.log(`    ${cyan("Backend:")}  http://127.0.0.1:8000 (API & /docs)`);
console.log(`    ${green("Frontend:")} http://localhost:3000`);
console.log(bold("==================================================\n"));

// 1. Detect Python executable
function getPythonCommand() {
  const isWin = process.platform === "win32";
  const venvPythonWin = path.join(backendDir, ".venv", "Scripts", "python.exe");
  const venvPythonUnix = path.join(backendDir, ".venv", "bin", "python");

  if (isWin && fs.existsSync(venvPythonWin)) return venvPythonWin;
  if (!isWin && fs.existsSync(venvPythonUnix)) return venvPythonUnix;

  return isWin ? "python" : "python3";
}

const pythonCmd = getPythonCommand();

// 2. Helper to pipe process output with prefix
function streamLogs(child, prefix, colorFn) {
  let stdoutBuffer = "";
  child.stdout.on("data", (chunk) => {
    stdoutBuffer += chunk.toString();
    const lines = stdoutBuffer.split(/\r?\n/);
    stdoutBuffer = lines.pop() ?? "";
    for (const line of lines) {
      if (line.trim()) {
        console.log(`${colorFn(`[${prefix}]`)} ${line}`);
      }
    }
  });

  let stderrBuffer = "";
  child.stderr.on("data", (chunk) => {
    stderrBuffer += chunk.toString();
    const lines = stderrBuffer.split(/\r?\n/);
    stderrBuffer = lines.pop() ?? "";
    for (const line of lines) {
      if (line.trim()) {
        console.error(`${colorFn(`[${prefix}]`)} ${line}`);
      }
    }
  });
}

// 3. Spawn Backend
const backendArgs = ["-m", "uvicorn", "app.main:app", "--reload", "--host", "127.0.0.1", "--port", "8000"];
const backendProcess = spawn(pythonCmd, backendArgs, {
  cwd: backendDir,
  env: { ...process.env, PYTHONUNBUFFERED: "1" },
  shell: process.platform === "win32",
});

streamLogs(backendProcess, "backend", cyan);

// 4. Spawn Frontend
const isWin = process.platform === "win32";
const npmCmd = isWin ? "npm.cmd" : "npm";
const frontendArgs = ["run", "dev", "--", "-p", "3000"];
const frontendProcess = spawn(npmCmd, frontendArgs, {
  cwd: rootDir,
  env: { ...process.env, FORCE_COLOR: "1" },
  shell: isWin,
});

streamLogs(frontendProcess, "frontend", green);

// 5. Graceful termination
let isShuttingDown = false;
function shutdown(signal = "SIGINT") {
  if (isShuttingDown) return;
  isShuttingDown = true;
  console.log(`\n${yellow(`Received ${signal}. Shutting down Saarathi development servers...`)}`);

  const killProcess = (child) => {
    if (!child || !child.pid) return;
    try {
      if (process.platform === "win32") {
        execSync(`taskkill /pid ${child.pid} /T /F 2>nul`);
      } else {
        process.kill(-child.pid, "SIGTERM");
      }
    } catch {
      try {
        child.kill("SIGKILL");
      } catch {}
    }
  };

  killProcess(backendProcess);
  killProcess(frontendProcess);

  console.log(green("All services stopped successfully. Goodbye!"));
  process.exit(0);
}

if (process.platform === "win32") {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  rl.on("SIGINT", () => shutdown("SIGINT"));
}

process.on("SIGINT", () => shutdown("SIGINT"));
process.on("SIGTERM", () => shutdown("SIGTERM"));
process.on("exit", () => shutdown("exit"));
