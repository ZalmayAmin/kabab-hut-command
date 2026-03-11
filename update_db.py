import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

try:
    # This is the line that fixes your specific error!
    cursor.execute('ALTER TABLE menu ADD COLUMN spice_level INTEGER DEFAULT 0')
    
    # You might also need this one for your 'is_featured' logic
    cursor.execute('ALTER TABLE menu ADD COLUMN is_featured INTEGER DEFAULT 0')
    
    conn.commit()
    print("Menu table updated successfully!")
except sqlite3.OperationalError as e:
    print(f"Operational error: {e}")
    # This likely means the columns already exist
    
conn.close()