import { describe, it, expect, beforeAll } from 'vitest';
import { experimental_AstroContainer as AstroContainer } from 'astro/container';
import LibraryPage from '../pages/library.astro';

describe('Library Page', () => {
  let container: AstroContainer;

  beforeAll(async () => {
    container = await AstroContainer.create();
  });

  it('should render the library page', async () => {
    const result = await container.renderToString(LibraryPage);
    expect(result).toContain('<html');
    expect(result).toContain('LIBRARY');
  });

  it('should have Library title', async () => {
    const result = await container.renderToString(LibraryPage);
    expect(result).toContain('<title>Library</title>');
  });

  it('should have search input', async () => {
    const result = await container.renderToString(LibraryPage);
    expect(result).toContain('id="book-search"');
    expect(result).toContain('placeholder=');
  });

  it('should have filter buttons', async () => {
    const result = await container.renderToString(LibraryPage);
    expect(result).toContain('filter-btn');
    expect(result).toContain('data-filter="all"');
    expect(result).toContain('data-filter="read"');
    expect(result).toContain('data-filter="reading"');
    expect(result).toContain('data-filter="to-read"');
  });

  it('should have book grid container', async () => {
    const result = await container.renderToString(LibraryPage);
    expect(result).toContain('book-grid');
  });

  it('should render book cards', async () => {
    const result = await container.renderToString(LibraryPage);
    expect(result).toContain('book-card');
    expect(result).toContain('book-cover');
    expect(result).toContain('book-title');
  });

  it('should have last updated info', async () => {
    const result = await container.renderToString(LibraryPage);
    expect(result).toContain('Last updated');
  });

  it('should credit Inventaire as source', async () => {
    const result = await container.renderToString(LibraryPage);
    expect(result).toContain('inventaire.io');
  });
});
