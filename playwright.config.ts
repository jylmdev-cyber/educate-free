import { defineConfig, devices } from '@playwright/test'
const baseURL = `http://127.0.0.1:4173${process.env.PAGES_BASE ?? '/educate-free/'}`
const evidenceDir = process.env.EVIDENCE_DIR ?? '.artifacts/e2e'
export default defineConfig({
  testDir: './tests/e2e', fullyParallel: true, reporter: [['list'], ['json', { outputFile: `${evidenceDir}/playwright.json` }]],
  use: { baseURL, channel: process.env.PLAYWRIGHT_CHANNEL as 'chrome' | 'msedge' | undefined, trace: 'retain-on-failure' },
  projects: [{ name: 'desktop', use: { ...devices['Desktop Chrome'] } }, { name: 'mobile', use: { ...devices['Pixel 7'] } }],
  webServer: { command: 'npm run preview -- --port 4173 --strictPort', url: baseURL, reuseExistingServer: !process.env.CI },
})
