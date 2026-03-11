import sqlite3

def reset_database():
    # Connect to your database file
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # 1. Wipe the old table completely
    print("Dropping old menu table...")
    cursor.execute('DROP TABLE IF EXISTS menu')

    # 2. Create the clean table (NO spice_level, NO is_featured)
    print("Creating fresh menu table...")
    cursor.execute('''
        CREATE TABLE menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL,
            image_url TEXT,
            category TEXT
        )
    ''')

    # 3. Add your actual menu items
    menu_items = [
        ('Paneer Tikka', 'Spiced cottage cheese cubes grilled to perfection.', 12.99, 'https://images.unsplash.com/photo-1567184109411-47a7a39485ed', 'Appetizers'),
        ('Chicken 65', 'Deep-fried spicy chicken tempered with curry leaves.', 13.99, 'https://images.unsplash.com/photo-1610057099443-fde8c4d50f91', 'Fry Items'),
        ('Signature Seekh Kabab', 'Minced lamb with herbs and traditional spices.', 15.99, 'https://images.unsplash.com/photo-1603360946369-dc9bb6258143', 'From the Grill'),
        ('Goat Biryani', 'Slow-cooked fragrant basmati rice with tender goat.', 18.99, 'https://images.unsplash.com/photo-1563379091339-03b21bc4a4f8', 'Biryani'),
        ('Garlic Naan', 'Freshly baked tandoori bread with garlic and butter.', 3.99, 'https://images.unsplash.com/photo-1601050648497-3f5dea97084c', 'Breads'),
        ('Mango Lassi', 'Refreshing yogurt drink with mango pulp.', 4.99, 'https://images.unsplash.com/photo-1546173159-315724a31696', 'Beverages & Drinks')
    ]

    cursor.executemany('''
        INSERT INTO menu (name, description, price, image_url, category) 
        VALUES (?, ?, ?, ?, ?)
    ''', menu_items)

    conn.commit()
    conn.close()
    print("✅ Database is now clean and items are added!")

if __name__ == "__main__":
    reset_database()