const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // 👇 Your public Notion page link
  const url = 'https://wasikhan.notion.site/Most-imp-Notion-page-will-take-me-into-jannah-IA-1b51284063e7805fb121cac3d3104bc3';

  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(5000); // wait for Notion to fully render

  const content = await page.evaluate(() => {
    return document.body.innerText;
  });

  fs.writeFileSync('notion.txt', content);
  await browser.close();

  console.log("✅ Notion content scraped.");
})();
