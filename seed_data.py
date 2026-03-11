import sqlite3

def seed_menu():
    conn = sqlite3.connect('kabab_hut.db')
    cursor = conn.cursor()
    
    # 1. Create the table with the new spice_level column
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            image_url TEXT,
            spice_level INTEGER DEFAULT 0,
            is_featured BOOLEAN DEFAULT 0
        )
    ''')
    
    cursor.execute("DELETE FROM menu")
    
    # 3. Insert fresh data (Name, Desc, Price, Category, Image, Spice_Level)
    # 0 = No Spice, 1 = Mild, 2 = Medium, 3 = Extra Hot
    menu_items = [
        ('Seekh Kabab Platter', 'Juicy minced beef skewers grilled over charcoal.', 15.99, 'Platters', 'https://images.unsplash.com/photo-1599487488170-d11ec9c175f0?q=80&w=800', 2),
        ('Butter Chicken', 'Creamy tomato-based curry with tender chicken pieces.', 14.99, 'Curries', 'https://images.unsplash.com/photo-1603894584714-73bc18afec49?q=80&w=800', 1),
        ('Garlic Naan', 'Freshly baked tandoori bread with garlic and parsley.', 3.50, 'Sides', 'https://images.unsplash.com/photo-1601050690597-df0568f70950?q=80&w=800', 0),
        ('Lamb Chops', 'Marinated lamb chops grilled to perfection.', 19.99, 'Platters', 'https://images.unsplash.com/photo-1544025162-d76694265947?q=80&w=800', 2),
        ('Mango Lassi', 'Traditional yogurt-based mango drink.', 4.50, 'Beverages', 'https://images.unsplash.com/photo-1571006682881-79262bc8644e?q=80&w=800', 0)
    ]
    
    cursor.executemany('''
        INSERT INTO menu (name, description, price, category, image_url, spice_level) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', menu_items)
    
    conn.commit()
    conn.close()
    print("Success! Spice levels added to the menu.")

if __name__ == "__main__":
    seed_menu()