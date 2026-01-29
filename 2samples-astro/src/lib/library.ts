export interface Book {
  title: string;
  author: string;
  cover: string | null;
  year: string | null;
  status: 'read' | 'reading' | 'to-read';
  rating: number | null;
  category: string;
  isbn: string | null;
}

export interface LibraryData {
  last_updated: string;
  source: string;
  books: Book[];
}

export async function loadLibraryData(): Promise<LibraryData> {
  try {
    const response = await fetch('/library_data.json');
    return await response.json();
  } catch {
    return {
      last_updated: 'N/A',
      source: 'none',
      books: [],
    };
  }
}
