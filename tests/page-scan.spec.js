/**
 * Auto-generated regression suite
 * Source:      Page Scan - Exploratory Tester (browser extension)
 * Target URL:  https://www.boat-lifestyle.com/?utm_source=google&utm_medium=cpc&utm_content=L%26F_boAt_D2C_Search-Brand_boat__Only_Prospecting_India_18%2F02%2F26&gad_source=1&gad_campaignid=23577249767&gbraid=0AAAAADCnhlzrHVmrQcsy4XVuWHmf6A0er&gclid=EAIaIQobChMInurXz-KMlwMVSSODAx27uTUUEAAYASAAEgIokvD_BwE
 * Generated:   2026-09-26T18:42:44.323Z
 *
 * These tests codify the checks the extension ran manually during
 * exploratory testing, so regressions get caught automatically on every
 * push instead of relying on someone re-running the manual scan.
 *
 * Run locally with:  npx playwright test
 */
const { test, expect } = require("@playwright/test");

const TARGET_URL = "https://www.boat-lifestyle.com/?utm_source=google&utm_medium=cpc&utm_content=L%26F_boAt_D2C_Search-Brand_boat__Only_Prospecting_India_18%2F02%2F26&gad_source=1&gad_campaignid=23577249767&gbraid=0AAAAADCnhlzrHVmrQcsy4XVuWHmf6A0er&gclid=EAIaIQobChMInurXz-KMlwMVSSODAx27uTUUEAAYASAAEgIokvD_BwE";

test.describe("Page Scan regression checks", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(TARGET_URL);
  });

  test("page loads within performance budget", async ({ page }) => {
    const start = Date.now();
    await page.goto(TARGET_URL, { waitUntil: "load" });
    const loadTime = Date.now() - start;
    expect(loadTime, "Page load time (ms)").toBeLessThan(4000);
  });

  test("has a non-empty <title> of reasonable length", async ({ page }) => {
    const title = await page.title();
    expect(title.length, "Title should not be empty").toBeGreaterThan(0);
    expect(title.length, "Title length should stay under 60 chars for SEO").toBeLessThanOrEqual(60);
  });

  test("has a meta description tag", async ({ page }) => {
    const desc = page.locator('meta[name="description"]');
    await expect(desc, "Missing <meta name=description>").toHaveCount(1);
    const content = await desc.getAttribute("content");
    expect(content && content.trim().length, "Meta description should not be empty").toBeGreaterThan(0);
  });

  test("has a meta viewport tag (mobile rendering)", async ({ page }) => {
    await expect(page.locator('meta[name="viewport"]')).toHaveCount(1);
  });

  test("has exactly one <h1>", async ({ page }) => {
    await expect(page.locator("h1")).toHaveCount(1);
  });

  test("all images have alt text", async ({ page }) => {
    const imagesWithoutAlt = await page.locator("img:not([alt]), img[alt='']").count();
    expect(imagesWithoutAlt, "Images missing alt text").toBe(0);
  });

  test("all form fields have an accessible label", async ({ page }) => {
    const unlabeled = await page
      .locator("input:not([type=hidden]):not([aria-label]):not([aria-labelledby])")
      .evaluateAll((els) =>
        els.filter((el) => !(el.id && document.querySelector(`label[for="${el.id}"]`)) && !el.closest("label")).length
      );
    expect(unlabeled, "Unlabeled form fields").toBe(0);
  });

  test("<html> declares a lang attribute", async ({ page }) => {
    const lang = await page.locator("html").getAttribute("lang");
    expect(lang, "Missing lang attribute on <html>").toBeTruthy();
  });

  test("previously-checked links still respond (not 4xx/5xx)", async ({ request }) => {
    const links = [
        "https://www.boat-lifestyle.com/?utm_source=google&utm_medium=cpc&utm_content=L%26F_boAt_D2C_Search-Brand_boat__Only_Prospecting_India_18%2F02%2F26&gad_source=1&gad_campaignid=23577249767&gbraid=0AAAAADCnhlzrHVmrQcsy4XVuWHmf6A0er&gclid=EAIaIQobChMInurXz-KMlwMVSSODAx27uTUUEAAYASAAEgIokvD_BwE#main",
        "https://www.boat-lifestyle.com/collections/daily-deals",
        "https://www.boat-lifestyle.com/?utm_source=google&utm_medium=cpc&utm_content=L%26F_boAt_D2C_Search-Brand_boat__Only_Prospecting_India_18%2F02%2F26&gad_source=1&gad_campaignid=23577249767&gbraid=0AAAAADCnhlzrHVmrQcsy4XVuWHmf6A0er&gclid=EAIaIQobChMInurXz-KMlwMVSSODAx27uTUUEAAYASAAEgIokvD_BwE#",
        "https://www.boat-lifestyle.com/collections/true-wireless-earbuds",
        "https://www.boat-lifestyle.com/collections/bluetooth-neckbands",
        "https://www.boat-lifestyle.com/collections/smart-watches",
        "https://www.boat-lifestyle.com/collections/wired-and-wireless-headphones",
        "https://www.boat-lifestyle.com/collections/wireless-speakers",
        "https://www.boat-lifestyle.com/collections/home-audio",
        "https://www.boat-lifestyle.com/collections/party-speakers",
        "https://www.boat-lifestyle.com/collections/power-banks",
        "https://www.boat-lifestyle.com/collections/dashcam",
        "https://www.boat-lifestyle.com/collections/cinehead-projectors",
        "https://www.boat-lifestyle.com/collections/slazer-trimmers",
        "https://www.boat-lifestyle.com/collections/immortal-gaming",
        "https://www.boat-lifestyle.com/collections/chargers-and-cables",
        "https://www.boat-lifestyle.com/collections/wired-earphones",
        "https://www.boat-lifestyle.com/collections/exclusive-limited-editions",
        "https://www.boat-lifestyle.com/collections/product-personalization",
        "https://www.boat-lifestyle.com/pages/bulk-orders",
        "https://www.boat-lifestyle.com/pages/gifting-with-boat",
        "https://www.boat-lifestyle.com/pages/boat-blogs",
        "https://www.boat-lifestyle.com/pages/refer-and-earn",
        "https://www.boat-lifestyle.com/pages/boat-careers",
        "https://www.boat-lifestyle.com/pages/find-store"
    ];
    for (const link of links) {
      const res = await request.head(link).catch(() => null);
      const status = res ? res.status() : 0;
      expect(status, `Broken link: ${link}`).toBeGreaterThan(0);
      expect(status, `Broken link: ${link}`).toBeLessThan(400);
    }
  });
});
