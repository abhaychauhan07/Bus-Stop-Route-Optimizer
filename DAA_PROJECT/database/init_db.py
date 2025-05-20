import sqlite3
import os

def init_db():
    # Create database directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect('bus_routes.db')
    c = conn.cursor()
    
    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS bus_stops (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source INTEGER NOT NULL,
            destination INTEGER NOT NULL,
            distance REAL NOT NULL,
            FOREIGN KEY (source) REFERENCES bus_stops (id),
            FOREIGN KEY (destination) REFERENCES bus_stops (id)
        )
    ''')
    
    # Insert sample data
    sample_stops = [
        (1, "Central Station", 18.5204, 73.8567),
        (2, "Shivaji Nagar", 18.5314, 73.8446),
        (3, "Deccan Gymkhana", 18.5236, 73.8478),
        (4, "FC Road", 18.5285, 73.8412),
        (5, "Kothrud Depot", 18.5041, 73.8124)
    ]
    
    sample_routes = [
        (1, 2, 2.5),
        (2, 3, 1.8),
        (3, 4, 1.2),
        (4, 5, 3.5),
        (1, 3, 3.0),
        (2, 4, 2.2),
        (3, 5, 4.1)
    ]
    
    c.executemany('INSERT OR REPLACE INTO bus_stops (id, name, latitude, longitude) VALUES (?, ?, ?, ?)', sample_stops)
    c.executemany('INSERT OR REPLACE INTO routes (source, destination, distance) VALUES (?, ?, ?)', sample_routes)
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!") 