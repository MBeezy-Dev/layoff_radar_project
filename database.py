import sqlite3
import json
import os
from datetime import datetime

class Database:
    def __init__(self, db_path="data/layoffs.db"):
        # Stelle sicher, dass der Ordner existiert
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT,
                location TEXT,
                affected_count INTEGER,
                notice_date DATE,
                layoff_date DATE,
                industry TEXT,
                source_url TEXT,
                unique_hash TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def insert_notice(self, data):
        try:
            self.cursor.execute("""
                INSERT INTO notices (company, location, affected_count, notice_date, layoff_date, industry, source_url, unique_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['company'], data['location'], data['affected_count'],
                data['notice_date'], data['layoff_date'], data['industry'],
                data['source_url'], data['unique_hash']
            ))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def export_to_json(self, output_path="data/web_export.json"):
        self.conn.row_factory = sqlite3.Row
        cur = self.conn.cursor()
        # Hole die neuesten 100 Einträge
        cur.execute("SELECT * FROM notices ORDER BY notice_date DESC LIMIT 100")
        rows = cur.fetchall()
        
        data = [dict(row) for row in rows]
        
        # Statistiken berechnen
        total_affected = sum(row['affected_count'] for row in data) if data else 0
        latest_date = data[0]['notice_date'] if data else "N/A"
        
        export_data = {
            "meta": {
                "generated_at": datetime.now().isoformat(),
                "total_records": len(data),
                "total_affected_7days": total_affected, # Simplifiziert
                "latest_update": latest_date
            },
            "data": data
        }
        
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)
            
    def close(self):
        self.conn.close()
