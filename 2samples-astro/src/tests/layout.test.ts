import { describe, it, expect, beforeAll } from 'vitest';
import { experimental_AstroContainer as AstroContainer } from 'astro/container';
import Base from '../layouts/Base.astro';

describe('Base Layout', () => {
  let container: AstroContainer;

  beforeAll(async () => {
    container = await AstroContainer.create();
  });

  it('should render document structure with html, head, and body', async () => {
    const result = await container.renderToString(Base, {
      slots: { default: '<p>Test content</p>' },
    });

    expect(result).toContain('<html');
    expect(result).toContain('<head>');
    expect(result).toContain('<body'); // Astro adds data attributes to body
  });

  it('should contain all navigation links', async () => {
    const result = await container.renderToString(Base, {
      slots: { default: '<p>Test content</p>' },
    });

    const navLinks = ['HOME', 'Japan', 'Ireland', 'UK', 'Greece', 'Bahamas', 'Blog', 'Maps', 'Library'];
    navLinks.forEach((link) => {
      expect(result).toContain(link);
    });
  });

  it('should have correct href attributes for nav links', async () => {
    const result = await container.renderToString(Base, {
      slots: { default: '<p>Test content</p>' },
    });

    expect(result).toContain('href="/"');
    expect(result).toContain('href="/japan"');
    expect(result).toContain('href="/ireland"');
    expect(result).toContain('href="/uk"');
    expect(result).toContain('href="/greece"');
    expect(result).toContain('href="/bahamas"');
    expect(result).toContain('href="/blog"');
    expect(result).toContain('href="/maps"');
    expect(result).toContain('href="/library"');
  });

  it('should have header with nav class', async () => {
    const result = await container.renderToString(Base, {
      slots: { default: '<p>Test content</p>' },
    });

    expect(result).toContain('class="header"');
  });

  it('should have stylesheet link', async () => {
    const result = await container.renderToString(Base, {
      slots: { default: '<p>Test content</p>' },
    });

    expect(result).toContain('<link');
    expect(result).toContain('stylesheet');
  });

  it('should render slot content', async () => {
    const testContent = '<div class="test-content">Hello World</div>';
    const result = await container.renderToString(Base, {
      slots: { default: testContent },
    });

    expect(result).toContain('test-content');
    expect(result).toContain('Hello World');
  });

  it('should have favicon link', async () => {
    const result = await container.renderToString(Base, {
      slots: { default: '<p>Test content</p>' },
    });

    expect(result).toContain('favicon');
  });
});
