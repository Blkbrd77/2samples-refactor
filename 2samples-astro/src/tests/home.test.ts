import { describe, it, expect, beforeAll } from 'vitest';
import { experimental_AstroContainer as AstroContainer } from 'astro/container';
import HomePage from '../pages/index.astro';

describe('Home Page', () => {
  let container: AstroContainer;

  beforeAll(async () => {
    container = await AstroContainer.create();
  });

  it('should render the home page', async () => {
    const result = await container.renderToString(HomePage);
    expect(result).toContain('<html');
  });

  it('should have HOME title', async () => {
    const result = await container.renderToString(HomePage);
    expect(result).toContain('<title>HOME</title>');
  });

  it('should render 6 destination tiles', async () => {
    const result = await container.renderToString(HomePage);
    const tileMatches = result.match(/class="tile"/g);
    expect(tileMatches).toHaveLength(6);
  });

  it('should have all destination tiles with correct content', async () => {
    const result = await container.renderToString(HomePage);

    // Check all destinations are present
    expect(result).toContain('JAPAN');
    expect(result).toContain('REPUBLIC OF IRELAND');
    expect(result).toContain('UNITED KINGDOM');
    expect(result).toContain('GREECE');
    expect(result).toContain('BAHAMAS');
    expect(result).toContain('OUR TRAVELS');
  });

  it('should have tile buttons with correct links', async () => {
    const result = await container.renderToString(HomePage);

    expect(result).toContain('href="/japan"');
    expect(result).toContain('href="/ireland"');
    expect(result).toContain('href="/uk"');
    expect(result).toContain('href="/greece"');
    expect(result).toContain('href="/bahamas"');
    expect(result).toContain('href="/maps"');
  });

  it('should have CloudFront image URLs', async () => {
    const result = await container.renderToString(HomePage);
    expect(result).toContain('https://d1rhrn7ca7di1b.cloudfront.net');
  });

  it('should have tile structure with image, h2, p, and button', async () => {
    const result = await container.renderToString(HomePage);

    // Each tile should have an image
    expect(result).toContain('<img');
    // Each tile should have an h2 (Astro adds data attributes)
    expect(result).toContain('<h2');
    // Each tile should have a paragraph
    expect(result).toContain('<p');
    // Each tile should have a button link
    expect(result).toContain('class="tile-button"');
  });
});
