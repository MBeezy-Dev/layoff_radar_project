from database import Database
from scrapers.ny_scraper import NYScraper

def run_job():
    print("--- LayoffRadar Scraper Started ---")
    db = Database()
    
    # Scraper registrieren
    scrapers = [NYScraper()]
    
    new_count = 0
    
    for scraper in scrapers:
        try:
            data = scraper.scrape()
            for entry in data:
                if db.insert_notice(entry):
                    print(f"[NEW] {entry['company']} in {entry['location']}")
                    new_count += 1
                else:
                    print(f"[SKIP] {entry['company']} (already exists)")
        except Exception as e:
            print(f"Error in scraper: {e}")
            
    # WICHTIG: JSON für die Website generieren
    print("Generating JSON export...")
    db.export_to_json()
    db.close()
    print(f"--- Job Done. {new_count} new records. ---")

if __name__ == "__main__":
    run_job()
