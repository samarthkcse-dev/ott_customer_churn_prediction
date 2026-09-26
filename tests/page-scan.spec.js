/**
 * Auto-generated regression suite
 * Source:      Page Scan - Exploratory Tester (browser extension)
 * Target URL:  https://github.com/samarthkcse-dev/ott_customer_churn_prediction/tree/master
 * Generated:   2026-09-26T19:07:14.473Z
 *
 * These tests codify the checks the extension ran manually during
 * exploratory testing, so regressions get caught automatically on every
 * push instead of relying on someone re-running the manual scan.
 *
 * Run locally with:  npx playwright test
 */
const { test, expect } = require("@playwright/test");

const TARGET_URL = "https://github.com/samarthkcse-dev/ott_customer_churn_prediction/tree/master";

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
        "https://github.com/samarthkcse-dev/ott_customer_churn_prediction/tree/master#start-of-content",
        "https://github.com/",
        "https://github.com/samarthkcse-dev",
        "https://github.com/samarthkcse-dev/ott_customer_churn_prediction",
        "https://github.com/copilot",
        "https://github.com/issues",
        "https://github.com/pulls",
        "https://github.com/repos",
        "https://github.com/notifications",
        "https://github.com/samarthkcse-dev/ott_customer_churn_prediction/issues",
        "https://github.com/samarthkcse-dev/ott_customer_churn_prediction/pulls",
        "https://github.com/samarthkcse-dev/ott_customer_churn_prediction/agents?author=samarthkcse-dev",
        "https://github.com/samarthkcse-dev/ott_customer_churn_prediction/actions",
        "https://github.com/samarthkcse-dev/ott_customer_churn_prediction/projects",
        "https://github.com/samarthkcse-dev/ott_customer_churn_prediction/wiki",
        "https://github.com/samarthkcse-dev/ott_customer_churn_prediction/security",
        "https://github.com/samarthkcse-dev/ott_customer_churn_prediction/pulse",
        "https://github.com/samarthkcse-dev/ott_customer_churn_prediction/settings",
        "https://github.com/samarthkcse-dev/ott_customer_churn_prediction/tree/master",
        "https://github.dev/",
        "https://github.com/codespaces/new/samarthkcse-dev/ott_customer_churn_prediction?resume=1",
        "https://github.com/samarthkcse-dev/ott_customer_churn_prediction/stargazers",
        "https://github.com/samarthkcse-dev/ott_customer_churn_prediction/forks",
        "https://github.com/samarthkcse-dev/ott_customer_churn_prediction/watchers",
        "https://github.com/samarthkcse-dev/ott_customer_churn_prediction/branches"
    ];
    for (const link of links) {
      const res = await request.head(link).catch(() => null);
      const status = res ? res.status() : 0;
      expect(status, `Broken link: ${link}`).toBeGreaterThan(0);
      expect(status, `Broken link: ${link}`).toBeLessThan(400);
    }
  });
});
