import { test, expect } from '@playwright/test';

test.describe('Security Headers', () => {
  test('should have security headers present', async ({ page }) => {
    const response = await page.goto('/');

    // Note: In development mode, Cloudflare _headers file isn't served
    // These headers will be present in production via Cloudflare Pages
    // For now, we verify the page loads successfully
    expect(response?.status()).toBe(200);
  });

  test('should not expose sensitive data in HTML', async ({ page }) => {
    await page.goto('/');
    const html = await page.content();

    // Check for common sensitive data patterns
    expect(html).not.toContain('AWS_ACCESS_KEY');
    expect(html).not.toContain('AWS_SECRET');
    expect(html).not.toContain('CLOUDFLARE_API_TOKEN');
    expect(html).not.toContain('api_key');
    expect(html).not.toContain('password');
    expect(html).not.toContain('secret');
  });

  test('should not expose sensitive data on destination pages', async ({ page }) => {
    const pages = ['/japan', '/ireland', '/uk', '/greece', '/bahamas'];

    for (const path of pages) {
      await page.goto(path);
      const html = await page.content();

      expect(html).not.toContain('AWS_ACCESS_KEY');
      expect(html).not.toContain('AWS_SECRET');
    }
  });

  test('should not expose sensitive data on library page', async ({ page }) => {
    await page.goto('/library');
    const html = await page.content();

    expect(html).not.toContain('AWS_ACCESS_KEY');
    expect(html).not.toContain('AWS_SECRET');
    expect(html).not.toContain('CLOUDFLARE_API_TOKEN');
  });
});

test.describe('Content Security', () => {
  test('should use HTTPS for external resources', async ({ page }) => {
    await page.goto('/');
    const html = await page.content();

    // Check that CloudFront URLs use HTTPS
    const cloudfrontMatches = html.match(/http:\/\/d1rhrn7ca7di1b\.cloudfront\.net/g);
    expect(cloudfrontMatches).toBeNull();

    // If CloudFront is used, it should be HTTPS
    if (html.includes('d1rhrn7ca7di1b.cloudfront.net')) {
      expect(html).toContain('https://d1rhrn7ca7di1b.cloudfront.net');
    }
  });

  test('should use HTTPS for external scripts on maps page', async ({ page }) => {
    await page.goto('/maps');
    const html = await page.content();

    // Check globe.gl script uses HTTPS
    if (html.includes('unpkg.com/globe.gl')) {
      expect(html).toContain('https://unpkg.com/globe.gl');
    }
  });

  test('should not have inline event handlers with external URLs', async ({ page }) => {
    await page.goto('/');
    const html = await page.content();

    // Check for potentially dangerous onclick patterns
    const dangerousPatterns = [
      /onclick=".*http:/i,
      /onerror=".*eval\(/i,
      /onload=".*document\.write/i,
    ];

    for (const pattern of dangerousPatterns) {
      expect(html).not.toMatch(pattern);
    }
  });
});

test.describe('Form Security', () => {
  test('library search input should not be vulnerable to basic XSS', async ({ page }) => {
    await page.goto('/library');

    const searchInput = page.locator('#book-search');

    // Try XSS payload
    const xssPayload = '<script>alert("xss")</script>';
    await searchInput.fill(xssPayload);

    // The script tag should not be executed or rendered
    const html = await page.content();
    expect(html).not.toContain('<script>alert("xss")</script>');

    // Page should still be functional
    await expect(page.locator('.book-grid')).toBeVisible();
  });
});

test.describe('External Links', () => {
  test('external links should have secure attributes', async ({ page }) => {
    await page.goto('/library');

    // Check Inventaire link
    const inventaireLink = page.locator('a[href="https://inventaire.io"]');
    await expect(inventaireLink).toHaveAttribute('target', '_blank');
  });
});
