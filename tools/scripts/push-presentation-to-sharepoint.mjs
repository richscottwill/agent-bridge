#!/usr/bin/env node
/**
 * Push leadership-demo-2026-05 folder to SharePoint Kiro-Drive/Artifacts/.
 *
 * Uses the SharePointTools class directly from the installed AmazonSharePointMCP package.
 * Run when SharePoint MCP auth is working (verify first with a list_libraries call in Kiro).
 *
 * Usage: node ~/shared/tools/scripts/push-presentation-to-sharepoint.mjs
 */

import { homedir } from 'os';
import { existsSync, readdirSync } from 'fs';
import { join } from 'path';

const SP_PKG = join(
  homedir(),
  'brazil-pkg-cache/packages/AmazonSharePointMCP/AmazonSharePointMCP-1.0.1331.0/AL2023_x86_64/DEV.STD.PTHREAD/build/amazon-sharepoint-mcp'
);
const { SharePointTools } = await import(join(SP_PKG, 'dist/tools/sharepoint-tools.js'));
const tools = new SharePointTools();

const LOCAL_DIR = join(homedir(), 'shared/presentations/leadership-demo-2026-05');
const SP_LIBRARY = 'Documents';
const SP_FOLDER = 'Kiro-Drive/Artifacts/leadership-demo-2026-05';
const PERSONAL = true;

if (!existsSync(LOCAL_DIR)) {
  console.error(`Local dir not found: ${LOCAL_DIR}`);
  process.exit(1);
}

// Ensure folder exists (idempotent — SharePoint MCP auto-creates parents)
console.error(`Creating folder: ${SP_FOLDER} in ${SP_LIBRARY} (personal=${PERSONAL})`);
try {
  await tools.createFolder(SP_LIBRARY, SP_FOLDER, undefined, PERSONAL);
  console.error('  ✓ folder ready');
} catch (e) {
  console.error(`  ⚠ folder create warning: ${e.message?.slice(0, 200)}`);
}

// Push every .md file in the folder
const files = readdirSync(LOCAL_DIR).filter(f => f.endsWith('.md'));
console.error(`\nPushing ${files.length} files...`);

const results = { ok: 0, fail: 0 };
for (const fileName of files) {
  const sourcePath = join(LOCAL_DIR, fileName);
  try {
    // writeFile signature: (libraryName, fileName, content, sourcePath, siteUrl, personal, folderPath, includeWebUrl)
    await tools.writeFile(SP_LIBRARY, fileName, undefined, sourcePath, undefined, PERSONAL, SP_FOLDER, false);
    console.error(`  ✓ ${fileName}`);
    results.ok++;
  } catch (e) {
    console.error(`  ✗ ${fileName}: ${e.message?.slice(0, 200)}`);
    results.fail++;
  }
}

console.error(`\nDone. ${results.ok} succeeded, ${results.fail} failed.`);
console.error(`Target: https://amazon-my.sharepoint.com/personal/prichwil_amazon_com/Documents/${SP_FOLDER.replace(/ /g, '%20')}`);
process.exit(results.fail > 0 ? 1 : 0);
