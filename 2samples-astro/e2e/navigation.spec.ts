import { test, expect } from '@playwright/test';

test.describe('Navigation', () => {
  test('should navigate to all main pages from home', async ({ page }) => {
    await page.goto('/');

    // Check home page loaded
    await expect(page).toHaveTitle('HOME');
    await expect(page.locator('nav.header')).toBeVisible();

    // Navigate to Japan
    await page.click('a[href="/japan"]');
    await expect(page).toHaveTitle('JAPAN');
    await expect(page.locator('h1').first()).toContainText('JAPAN');

    // Navigate to Ireland
    await page.click('a[href="/ireland"]');
    await expect(page).toHaveTitle('REPUBLIC OF IRELAND');

    // Navigate to UK
    await page.click('a[href="/uk"]');
    await expect(page).toHaveTitle('UNITED KINGDOM');

    // Navigate to Greece
    await page.click('a[href="/greece"]');
    await expect(page).toHaveTitle('GREECE');

    // Navigate to Bahamas
    await page.click('a[href="/bahamas"]');
    await expect(page).toHaveTitle('BAHAMAS');

    // Navigate to Blog
    await page.click('a[href="/blog"]');
    await expect(page).toHaveTitle('Blog');

    // Navigate to Maps
    await page.click('a[href="/maps"]');
    await expect(page).toHaveTitle('Travel Map');

    // Navigate to Library
    await page.click('a[href="/library"]');
    await expect(page).toHaveTitle('Library');

    // Navigate back to Home
    await page.click('a[href="/"]');
    await expect(page).toHaveTitle('HOME');
  });

  test('should have all navigation links visible', async ({ page }) => {
    await page.goto('/');

    const nav = page.locator('nav.header');
    await expect(nav.locator('a[href="/"]')).toBeVisible();
    await expect(nav.locator('a[href="/japan"]')).toBeVisible();
    await expect(nav.locator('a[href="/ireland"]')).toBeVisible();
    await expect(nav.locator('a[href="/uk"]')).toBeVisible();
    await expect(nav.locator('a[href="/greece"]')).toBeVisible();
    await expect(nav.locator('a[href="/bahamas"]')).toBeVisible();
    await expect(nav.locator('a[href="/blog"]')).toBeVisible();
    await expect(nav.locator('a[href="/maps"]')).toBeVisible();
    await expect(nav.locator('a[href="/library"]')).toBeVisible();
  });
});

test.describe('Home Page', () => {
  test('should display all destination tiles', async ({ page }) => {
    await page.goto('/');

    // Check all tiles are present
    const tiles = page.locator('.tile');
    await expect(tiles).toHaveCount(6);

    // Check specific destinations
    await expect(page.locator('.tile:has-text("Japan")')).toBeVisible();
    await expect(page.locator('.tile:has-text("Ireland")')).toBeVisible();
    await expect(page.locator('.tile:has-text("UK")')).toBeVisible();
    await expect(page.locator('.tile:has-text("Greece")')).toBeVisible();
    await expect(page.locator('.tile:has-text("Our Travels")')).toBeVisible();
    await expect(page.locator('.tile:has-text("Bahamas")')).toBeVisible();
  });

  test('should navigate from tile to destination page', async ({ page }) => {
    await page.goto('/');

    // Click on Japan tile button
    await page.locator('.tile:has-text("Japan") .tile-button').click();
    await expect(page).toHaveTitle('JAPAN');
  });
});

test.describe('Destination Pages', () => {
  const destinations = [
    { path: '/japan', title: 'JAPAN', heading: 'JAPAN' },
    { path: '/ireland', title: 'REPUBLIC OF IRELAND', heading: 'REPUBLIC OF IRELAND' },
    { path: '/uk', title: 'UNITED KINGDOM', heading: 'UNITED KINGDOM' },
    { path: '/greece', title: 'GREECE', heading: 'GREECE' },
    { path: '/bahamas', title: 'BAHAMAS', heading: 'BAHAMAS' },
  ];

  for (const dest of destinations) {
    test(`should render ${dest.title} page with video sections`, async ({ page }) => {
      await page.goto(dest.path);

      await expect(page).toHaveTitle(dest.title);
      await expect(page.locator('h1').first()).toContainText(dest.heading);

      // Check video sections exist
      const videoSections = page.locator('.video-container');
      await expect(videoSections.first()).toBeVisible();

      // Check video element exists
      const videos = page.locator('video');
      await expect(videos.first()).toBeVisible();
    });
  }

  test('video should have controls and poster', async ({ page }) => {
    await page.goto('/japan');

    const video = page.locator('video').first();
    await expect(video).toHaveAttribute('controls');
    await expect(video).toHaveAttribute('poster');
  });
});

test.describe('Library Page', () => {
  test('should display library with books', async ({ page }) => {
    await page.goto('/library');

    await expect(page).toHaveTitle('Library');
    await expect(page.locator('h1').first()).toContainText('LIBRARY');

    // Check book grid exists
    const bookGrid = page.locator('.book-grid');
    await expect(bookGrid).toBeVisible();

    // Check book cards exist
    const bookCards = page.locator('.book-card');
    await expect(bookCards.first()).toBeVisible();
  });

  test('should have working filter buttons', async ({ page }) => {
    await page.goto('/library');

    // Check filter buttons exist
    const filterButtons = page.locator('.filter-btn');
    await expect(filterButtons).toHaveCount(4);

    // Click on "Read" filter
    await page.click('.filter-btn[data-filter="read"]');
    await expect(page.locator('.filter-btn[data-filter="read"]')).toHaveClass(/active/);

    // Click on "Reading" filter
    await page.click('.filter-btn[data-filter="reading"]');
    await expect(page.locator('.filter-btn[data-filter="reading"]')).toHaveClass(/active/);

    // Click on "All" to reset
    await page.click('.filter-btn[data-filter="all"]');
    await expect(page.locator('.filter-btn[data-filter="all"]')).toHaveClass(/active/);
  });

  test('should have working search input', async ({ page }) => {
    await page.goto('/library');

    const searchInput = page.locator('#book-search');
    await expect(searchInput).toBeVisible();

    // Type in search
    await searchInput.fill('test search');
    await expect(searchInput).toHaveValue('test search');

    // Clear with Escape
    await searchInput.press('Escape');
    await expect(searchInput).toHaveValue('');
  });

  test('should show book count', async ({ page }) => {
    await page.goto('/library');

    const visibleCount = page.locator('#visible-count');
    await expect(visibleCount).toBeVisible();
    await expect(visibleCount).toContainText('books');
  });
});

test.describe('Maps Page', () => {
  test('should display maps page with globe container', async ({ page }) => {
    await page.goto('/maps');

    await expect(page).toHaveTitle('Travel Map');
    await expect(page.locator('h1').first()).toContainText("Where We've Been");

    // Check globe container exists
    const globeContainer = page.locator('#globe');
    await expect(globeContainer).toBeVisible();
  });
});

test.describe('Blog Page', () => {
  test('should display blog page', async ({ page }) => {
    await page.goto('/blog');

    await expect(page).toHaveTitle('Blog');
    await expect(page.locator('h1').first()).toContainText('BLOG');
  });
});

test.describe('Mobile Responsive', () => {
  test.use({ viewport: { width: 375, height: 667 } });

  test('should display navigation on mobile', async ({ page }) => {
    await page.goto('/');

    // Navigation should still be visible
    const nav = page.locator('nav.header');
    await expect(nav).toBeVisible();
  });

  test('should display tiles on mobile', async ({ page }) => {
    await page.goto('/');

    const tiles = page.locator('.tile');
    await expect(tiles.first()).toBeVisible();
  });

  test('should display library on mobile', async ({ page }) => {
    await page.goto('/library');

    const bookGrid = page.locator('.book-grid');
    await expect(bookGrid).toBeVisible();
  });
});
