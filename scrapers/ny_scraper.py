import hashlib
import random
from datetime import datetime, timedelta
from .base import BaseScraper

class NYScraper(BaseScraper):
    # Simuliert New York State WARN Notices
    URL = "https://dol.ny.gov/warn-notices"

    def scrape(self):
        print("   -> Scrape NY Data...")
        results = []
        
        # MOCK DATEN GENERATOR (Damit du auf der Website was siehst)
        # In Produktion hier: requests.get() und BeautifulSoup logic
        
        companies = ["TechFlow Solutions", "Global Logistics NY", "Urban Eat Corp", "Finance Partners LLC", "Hudson Valley Manufacturing"]
        cities = ["New York, NY", "Albany, NY", "Buffalo, NY", "Rochester, NY"]
        
        # Wir generieren dynamisch Daten basierend auf dem heutigen Tag
        # Damit der Bot immer mal was neues "findet"
        today = datetime.now()
        
        for i in range(3): 
            # Erzeugt Pseudo-Zufallsdaten, die sich täglich ändern
            day_offset = i
            date_str = (today - timedelta(days=day_offset)).strftime("%Y-%m-%d")
            
            comp = companies[i % len(companies)]
            loc = cities[i % len(cities)]
            count = (i + 1) * 42
            
            # Hash erstellen
            raw_string = f"{comp}{date_str}{count}"
            unique_hash = hashlib.md5(raw_string.encode()).hexdigest()
            
            entry = {
                "company": comp,
                "location": loc,
                "affected_count": count,
                "notice_date": date_str,
                "layoff_date": (today + timedelta(days=60)).strftime("%Y-%m-%d"),
                "industry": "Mixed",
                "source_url": self.URL,
                "unique_hash": unique_hash
            }
            results.append(entry)
            
        return results
