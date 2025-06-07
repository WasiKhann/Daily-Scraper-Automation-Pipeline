const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  const url = 'https://wasikhan.notion.site/Most-imp-Notion-page-will-take-me-into-jannah-IA-1b51284063e7805fb121cac3d3104bc3';
  await page.goto(url, { waitUntil: 'domcontentloaded' });

  await page.waitForTimeout(5000); // ensure content loads

  const raw = await page.evaluate(() => document.body.innerText);

  // Add line breaks around `..` marker
  const content = raw.replace(/\n?\.\.\n?/g, '\n..\n');

  fs.writeFileSync('notion.txt', content);
  console.log("✅ Notion content scraped and processed.");

  await browser.close();
})();
