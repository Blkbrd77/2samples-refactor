#!/usr/bin/env python3
"""
Fetch library data from Inventaire API and save to JSON.
This script can be run manually or via GitHub Action to refresh the cache.
"""

import json
import requests
from datetime import datetime
from pathlib import Path

# Configuration
INVENTAIRE_USER_ID = "f9a685e15825d73108b49c3465224b03"
OUTPUT_PATH = Path(__file__).parent.parent / "app" / "static" / "library_data.json"

def fetch_items(user_id, limit=500):
    """Fetch all items for a user from Inventaire API."""
    url = f"https://inventaire.io/api/items?action=by-users&users={user_id}&limit={limit}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def fetch_entities(uris):
    """Fetch entity details (title, author, cover) for multiple URIs."""
    if not uris:
        return {}
    # Inventaire API accepts comma-separated URIs
    uri_string = "|".join(uris[:50])  # Batch up to 50 at a time
    url = f"https://inventaire.io/api/entities?action=by-uris&uris={uri_string}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("entities", {})

def get_cover_url(entity):
    """Extract cover image URL from entity data."""
    image = entity.get("image", {})
    if isinstance(image, dict) and image.get("url"):
        url = image["url"]
        # Convert relative Inventaire URLs to absolute
        if url.startswith("/img/"):
            return f"https://inventaire.io{url}"
        return url
    # Try to get from claims (invp:P2 is Inventaire image property)
    claims = entity.get("claims", {})
    if "invp:P2" in claims:
        img_hash = claims["invp:P2"][0]
        return f"https://inventaire.io/img/entities/{img_hash}"
    if "wdt:P18" in claims:
        filename = claims["wdt:P18"][0]
        return f"https://commons.wikimedia.org/wiki/Special:FilePath/{filename}?width=200"
    # Fallback to Open Library cover by ISBN
    uri = entity.get("uri", "")
    if uri.startswith("isbn:"):
        isbn = uri.replace("isbn:", "")
        return f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
    return None

def get_title(entity):
    """Extract title from entity data."""
    # Try labels first
    labels = entity.get("labels", {})
    if isinstance(labels, dict):
        # Try common label keys
        for key in ["en", "fromclaims", "original"]:
            if key in labels:
                return labels[key]
        # Return first available label
        if labels:
            return list(labels.values())[0]

    # Try claims (P1476 is title property)
    claims = entity.get("claims", {})
    if "wdt:P1476" in claims:
        return claims["wdt:P1476"][0]

    return entity.get("label", "Unknown Title")

def get_author_name(entity, all_entities):
    """Extract author name from entity."""
    claims = entity.get("claims", {})

    # For editions, get the work first, then author from work
    work_uris = claims.get("wdt:P629", [])  # P629 is "edition of" (links to work)
    if work_uris and work_uris[0] in all_entities:
        work_entity = all_entities[work_uris[0]]
        work_claims = work_entity.get("claims", {})
        author_uris = work_claims.get("wdt:P50", [])
        if author_uris and author_uris[0] in all_entities:
            author_entity = all_entities[author_uris[0]]
            # Get author label
            labels = author_entity.get("labels", {})
            if isinstance(labels, dict):
                for key in ["en", "original"]:
                    if key in labels:
                        return labels[key]
                if labels:
                    return list(labels.values())[0]
            return author_entity.get("label", "Unknown Author")

    # Direct author on entity
    author_uris = claims.get("wdt:P50", [])
    if author_uris and author_uris[0] in all_entities:
        author_entity = all_entities[author_uris[0]]
        labels = author_entity.get("labels", {})
        if isinstance(labels, dict) and labels:
            return list(labels.values())[0]
        return author_entity.get("label", "Unknown Author")

    # Check for author string
    if "wdt:P2093" in claims:
        return claims["wdt:P2093"][0]

    return "Unknown Author"

def get_publication_year(entity):
    """Extract publication year from entity."""
    claims = entity.get("claims", {})
    pub_date = claims.get("wdt:P577", [None])[0]  # P577 is publication date
    if pub_date:
        return pub_date[:4]  # Extract year from date string
    return None

def get_category(entity):
    """Determine book category/genre."""
    claims = entity.get("claims", {})
    genres = claims.get("wdt:P136", [])  # P136 is genre
    subjects = claims.get("wdt:P921", [])  # P921 is main subject

    # Simple categorization based on common patterns
    label = entity.get("label", "").lower()
    description = entity.get("description", "").lower()

    if any(word in label + description for word in ["theology", "bible", "christian", "god", "jesus", "faith"]):
        return "Theology"
    elif any(word in label + description for word in ["philosophy", "philosophical"]):
        return "Philosophy"
    elif any(word in label + description for word in ["novel", "fiction", "mystery"]):
        return "Fiction"
    elif any(word in label + description for word in ["history", "historical"]):
        return "History"
    elif any(word in label + description for word in ["science", "physics", "biology"]):
        return "Science"
    else:
        return "General"

def transform_to_library_format(items_data, entities):
    """Transform Inventaire data to our library JSON format."""
    books = []

    for item in items_data.get("items", []):
        entity_uri = item.get("entity")
        if not entity_uri or entity_uri not in entities:
            continue

        entity = entities[entity_uri]

        # Determine reading status from item data
        transaction = item.get("transaction", "inventorying")
        listing = item.get("listing", "private")

        # Map to our status format
        if transaction == "giving" or transaction == "lending":
            status = "read"
        elif transaction == "selling":
            status = "read"
        else:
            status = "read"  # Default to read for inventoried items

        book = {
            "title": get_title(entity),
            "author": get_author_name(entity, entities),
            "cover": get_cover_url(entity),
            "year": get_publication_year(entity),
            "status": status,
            "rating": None,  # Inventaire doesn't have ratings
            "category": get_category(entity),
            "isbn": entity_uri.replace("isbn:", "") if entity_uri.startswith("isbn:") else None
        }
        books.append(book)

    return books

def main():
    print(f"Fetching items for user {INVENTAIRE_USER_ID}...")
    items_data = fetch_items(INVENTAIRE_USER_ID)
    total_items = items_data.get("total", 0)
    print(f"Found {total_items} items")

    # Collect all entity URIs
    entity_uris = [item.get("entity") for item in items_data.get("items", []) if item.get("entity")]
    print(f"Fetching details for {len(entity_uris)} entities...")

    # Fetch entities in batches
    all_entities = {}
    for i in range(0, len(entity_uris), 50):
        batch = entity_uris[i:i+50]
        print(f"  Fetching edition batch {i//50 + 1}...")
        entities = fetch_entities(batch)
        all_entities.update(entities)

    print(f"Retrieved {len(all_entities)} edition details")

    # Collect work URIs from editions (P629 = edition of)
    work_uris = set()
    for entity in all_entities.values():
        claims = entity.get("claims", {})
        for work_uri in claims.get("wdt:P629", []):
            work_uris.add(work_uri)

    print(f"Fetching {len(work_uris)} work entities...")
    work_uris = list(work_uris)
    for i in range(0, len(work_uris), 50):
        batch = work_uris[i:i+50]
        print(f"  Fetching work batch {i//50 + 1}...")
        entities = fetch_entities(batch)
        all_entities.update(entities)

    # Collect author URIs from works (P50 = author)
    author_uris = set()
    for entity in all_entities.values():
        claims = entity.get("claims", {})
        for author_uri in claims.get("wdt:P50", []):
            author_uris.add(author_uri)

    print(f"Fetching {len(author_uris)} author entities...")
    author_uris = list(author_uris)
    for i in range(0, len(author_uris), 50):
        batch = author_uris[i:i+50]
        print(f"  Fetching author batch {i//50 + 1}...")
        entities = fetch_entities(batch)
        all_entities.update(entities)

    print(f"Retrieved {len(all_entities)} total entity details")

    # Transform to our format
    books = transform_to_library_format(items_data, all_entities)
    print(f"Transformed {len(books)} books")

    # Build output
    library_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "source": "inventaire",
        "inventaire_user": INVENTAIRE_USER_ID,
        "books": books
    }

    # Save to file
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(library_data, f, indent=2)

    print(f"Saved {len(books)} books to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
