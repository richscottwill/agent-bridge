#!/usr/bin/env node
/**
 * SharePoint Durability Sync — Upload AM-Backend output files to SharePoint OneDrive.
 * 
 * Uses the SharePointTools class directly from the installed AmazonSharePointMCP package.
 * Non-blocking: logs warnings on failure and continues with remaining files.
 */

import { homedir } from 'os';
import { existsSync, readdirSync } from 'fs';
import { join } from 'path';

const SP_PKG = join(homedir(), 'brazil-pkg-cache/packages/AmazonSharePointMCP/AmazonSharePointMCP-1.0.1152.0/AL2023_x86_64/DEV.STD.PTHREAD/build/amazon-sharepoint-mcp');

const { SharePointTools } = await import(join(SP_PKG, 'dist/tools/sharepoint-tools.js'));
const tools = new SharePointTools();

// Files to push to Kiro-Drive/system-state/
const SYSTEM_STATE_FILES = [
  'am-enrichment-queue.json',
  'am-portfolio-findings.json',
  'am-abps-ai-state.json',
  'am-signals-processed.json',
];

const ACTIVE_DIR = join(homedir(), 'shared/context/active');
const STATE_FILES_DIR = join(homedir(), 'shared/wiki/state-files');

const results = { files_pushed: 0, files_failed: 0, details: [] };

// Upload a single file
async function uploadFile(libraryName, fileName, sourcePath, folderPath) {
  try {
    const result = await tools.writeFile(libraryName, fileName, undefined, sourcePath, undefined, true, folderPath);
    results.files_pushed++;
    results.details.push(`OK: ${folderPath}/${fileName}`);
    console.error(`  ✓ ${folderPath}/${fileName}`);
    return true;
  } catch (e) {
    results.files_failed++;
    const msg = e.message?.slice(0, 120) || 'unknown error';
    results.details.push(`FAIL: ${folderPath}/${fileName} — ${msg}`);
    console.error(`  ✗ ${folderPath}/${fileName}: ${msg}`);
    return false;
  }
}

// 1. Upload core AM files to Kiro-Drive/system-state/
console.error('Phase 1: Uploading AM-Backend core files to Kiro-Drive/system-state/');
for (const fileName of SYSTEM_STATE_FILES) {
  const sourcePath = join(ACTIVE_DIR, fileName);
  if (!existsSync(sourcePath)) {
    results.files_failed++;
    results.details.push(`MISSING: ${sourcePath}`);
    console.error(`  ⚠ MISSING: ${sourcePath}`);
    continue;
  }
  await uploadFile('Documents', fileName, sourcePath, 'Kiro-Drive/system-state');
}

// 2. Upload state files to Kiro-Drive/state-files/
console.error('Phase 2: Uploading state files to Kiro-Drive/state-files/');
if (existsSync(STATE_FILES_DIR)) {
  const stateFiles = readdirSync(STATE_FILES_DIR)
    .filter(f => f.endsWith('-state.md') || f.endsWith('-state.docx'))
    .sort();
  
  for (const fileName of stateFiles) {
    const sourcePath = join(STATE_FILES_DIR, fileName);
    await uploadFile('Documents', fileName, sourcePath, 'Kiro-Drive/state-files');
  }
} else {
  console.error('  ⚠ State files directory not found');
}

// Output JSON results
console.log(JSON.stringify(results));
