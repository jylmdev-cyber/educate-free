import { execFileSync } from 'node:child_process'
import { readFileSync, statSync } from 'node:fs'
import path from 'node:path'

// Inspect tracked and non-ignored candidates. Findings never print matched secret values.
let files
try {
  files = [...new Set(execFileSync('git', ['ls-files', '--cached', '--others', '--exclude-standard', '-z'], { encoding: 'utf8' }).split('\0').filter(Boolean))]
} catch {
  console.error('Repository check requires an initialized Git repository. Run git init -b main first.')
  process.exit(1)
}
const forbidden = /(?:^|\/)(?:node_modules|dist|test-results|playwright-report|\.artifacts|__pycache__)(?:\/|$)|^\.pallaquino\/(?:evidence|runtime|repository)\/|^\.pallaquino\/continuity\/checkpoints\/|^\.pallaquino\/execution\/file_locks\.json$|^design-qa\.md$|(?:^|\/)\.env(?:\.|$)(?!example$)|\.(?:pem|key|p12|pfx|tsbuildinfo|pyc)$|(?:^|\/)educalibre-progreso-.*\.json$/i
const patterns = [
  ['private-key', /-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----/],
  ['github-token', /\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{50,})\b/],
  ['provider-key', /\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{40,}\b/],
  ['aws-access-key', /\b(?:AKIA|ASIA)[A-Z0-9]{16}\b/],
  ['credential-in-url', /https?:\/\/[^\s/:'"]+:[^\s/@'"]+@/],
]
const findings = []
const allowedTestFixtures = []
let bytes = 0
let largest = { path: '', bytes: 0 }
for (const file of files) {
  if (forbidden.test(file)) findings.push({ path: file, rule: 'forbidden-generated-or-private-file' })
  const resolved = path.resolve(file)
  if (!resolved.startsWith(`${process.cwd()}${path.sep}`)) {
    findings.push({ path: file, rule: 'path-outside-workspace' })
    continue
  }
  let stat
  try { stat = statSync(resolved) } catch { continue } // Deletions may still be staged.
  if (!stat.isFile()) continue
  bytes += stat.size
  if (stat.size > largest.bytes) largest = { path: file, bytes: stat.size }
  if (stat.size > 50 * 1024 * 1024) findings.push({ path: file, rule: 'file-over-50-MiB' })
  if (stat.size > 2 * 1024 * 1024 || /\.(?:png|jpg|jpeg|webp|gif|ico|pdf|woff2?|zip)$/i.test(file)) continue
  const text = readFileSync(resolved, 'utf8')
  for (const [rule, pattern] of patterns) {
    for (const match of text.matchAll(new RegExp(pattern.source, 'g'))) {
      const line = text.slice(0, match.index).split('\n').length
      const fixtureUrl = 'https://' + 'user:pass' + '@example.com'
      if (file === 'tests/catalog.test.ts' && rule === 'credential-in-url' && text.startsWith(fixtureUrl, match.index) && /['"]/.test(text.charAt(match.index + fixtureUrl.length))) {
        allowedTestFixtures.push({ path: file, rule, line, reason: 'Exact inert example.com fixture verifies rejection of credential URLs' })
        continue
      }
      findings.push({ path: file, rule, line })
    }
  }
}
console.log(JSON.stringify({ result: findings.length ? 'FAIL' : 'PASS_SCOPED', candidateFiles: files.length, totalBytes: bytes, largest, findings, allowedTestFixtures, scope: 'Known token/private-key patterns and generated/private paths; not an exhaustive secret audit' }, null, 2))
process.exitCode = findings.length ? 1 : 0
