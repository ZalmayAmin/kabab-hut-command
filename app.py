import os
import sqlite3
import json
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from datetime import datetime
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "company-secret-key-123" 
DB_PATH = "kabab_hut.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL, 
    description TEXT, 
    price REAL NOT NULL, 
    special_price REAL,
    category TEXT NOT NULL, 
    image_url TEXT, 
    is_featured BOOLEAN DEFAULT 0,
    is_available BOOLEAN DEFAULT 1,
    is_special BOOLEAN DEFAULT 0)''')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS inquiries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    event_type TEXT,
    guest_count INTEGER,
    event_date TEXT,
    message TEXT,
    status TEXT DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    conn.execute('''CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    items_json TEXT NOT NULL,
    total_price TEXT NOT NULL,
    payment_method TEXT DEFAULT 'Cash',  -- NEW COLUMN
    status TEXT DEFAULT 'New',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    count = conn.execute('SELECT COUNT(*) FROM menu').fetchone()[0]
    if count < 30: 
        conn.execute('DELETE FROM menu')
        # name, desc, price, cat, img, is_featured, is_available
        expanded_items = [
            # APPETIZERS
            ('Vegetable Samosas', 'Two crispy pastries filled with spiced potatoes.', 7.99, 'Appetizers','https://therecipespk.com/wp-content/uploads/2016/06/Vegetable-Samosa-Recipe.jpg', 0, 1),
            ('Mixed Pakora', 'Assorted vegetable fritters in seasoned gram flour.', 9.99, 'Appetizers', 'https://food.fnr.sndimg.com/content/dam/images/food/fullset/2019/1/07/0/FNK_Mixed-Vegetable-Pakoras_s4x3.jpg.rend.hgtvcom.1280.960.suffix/1546894450671.webp', 0, 1),
            ('Paneer Tikka', 'Grilled cubes of cottage cheese with pickling spices.', 13.99, 'Appetizers', 'https://lentillovingfamily.com/wp-content/uploads/2025/08/paneer-tikka-2.jpg', 0, 1),
            ('Dahi Bhalla', 'Soft lentil dumplings soaked in spiced yogurt.', 8.99, 'Appetizers', 'https://ministryofcurry.com/wp-content/uploads/2016/08/Dahi-Vada-5.jpg', 0, 1),

            # FRY ITEMS
            ('Crispy Finger Fish', 'Breaded fish strips served with tangy tartar sauce.', 14.99, 'Fry Items', 'https://recipesblob.oetker.com.my/assets/1a8b3509bc274c71be2d0821946d1db1/1272x764/breadcrumbs-breadedfishfingers-eng.webp', 0, 1),
            ('Lahori Fish Bites', 'Deep-fried fish marinated in traditional Lahori spices.', 12.99, 'Fry Items', 'https://www.hassansquarefish.com/image/cache/catalog/products/0014-1-1000x1000.jpg', 0, 1),
            ('Chicken Lollipop', 'Chicken wings frenched and fried in a spicy red batter.', 13.99, 'Fry Items', 'https://iheartumami.com/wp-content/uploads/2023/04/chicken-lollipop-recipe-500x500.jpg', 0, 1),
            ('Golden Fried Prawns', 'Jumbo prawns battered and fried to a golden crisp.', 18.99, 'Fry Items', 'https://media.istockphoto.com/id/186139921/photo/fried-organic-coconut-shrimp.jpg?s=612x612&w=0&k=20&c=3xWq4C2JK0FfY0nJtkCwfs_KQedEXM-ERDVnEP_wqzo=', 1, 1),

            # FROM THE GRILL
            ('Lamb Premium Chops', 'Tender chops seasoned with Himalayan salt.', 24.99, 'From the Grill', 'https://t4.ftcdn.net/jpg/16/51/06/75/360_F_1651067585_SdZQUBacmJLnJUCyQr56vu6s0OIEzEnn.jpg', 1, 1),
            ('Chicken Malai Tikka', 'Creamy chicken morsels with white pepper.', 16.99, 'From the Grill', 'https://www.mirchitales.com/wp-content/uploads/2022/10/Malai_Tikka_Malai_Boti-4.jpg', 1, 1),
            ('Beef Bihari Boti', 'Smokey beef strips marinated in mustard oil.', 17.99, 'From the Grill', 'https://i.pinimg.com/736x/ce/01/8b/ce018be87476409627311765f5f95074.jpg', 1, 1),
            ('Reshmi Seekh Kabab', 'Minced chicken blended with silken herbs.', 14.99, 'From the Grill', 'https://courtyardcafe.pk/wp-content/uploads/2024/06/Reshmui-Kabab.jpg', 1, 1),
            ('Tandoori Whole Chicken', 'Full chicken marinated in yogurt and charred.', 22.99, 'From the Grill', 'https://www.easycookingwithmolly.com/wp-content/uploads/2023/11/air-fryer-whole-tandoori-chicken-3.jpg', 0, 1),

            # KABAB ROLLS
            ('Chicken Tikka Roll', 'Grilled chicken wrapped in a fresh paratha.', 11.99, 'Kabab Rolls', 'https://www.indianhealthyrecipes.com/wp-content/uploads/2024/02/chicken-kathi-roll-chicken-frankie.jpg', 0, 1),
            ('Seekh Kabab Roll', 'Minced beef kabab with onions and mint sauce.', 12.99, 'Kabab Rolls', 'https://i.pinimg.com/736x/c8/29/6f/c8296f9e011f3e8dbd72a768e4b539fe.jpg', 0, 1),
            ('Bihari Boti Roll', 'Tender beef bihari strips in a toasted wrap.', 13.99, 'Kabab Rolls', 'https://i.ytimg.com/vi/R6a8RJ1LgTs/maxresdefault.jpg', 0, 1),
            ('Paneer Mayo Roll', 'Grilled cottage cheese with garlic mayo and herbs.', 10.99, 'Kabab Rolls', 'https://instamart-media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,h_960,w_960//InstamartAssets/Receipes/potato_paneer_cheese_roll.webp', 0, 1),

            # NON-VEG CURRIES
            ('Butter Chicken', 'Tandoori chicken in a smooth tomato cream gravy.', 17.99, 'Non-Veg Curries', 'https://www.licious.in/blog/wp-content/uploads/2020/10/butter-chicken--600x600.jpg', 1, 1),
            ('Mutton Karahi', 'Goat meat cooked in a wok with fresh ginger.', 21.99, 'Non-Veg Curries', 'https://i.pinimg.com/736x/dc/9c/b0/dc9cb0bf4e3336dce6a965ba53439a0d.jpg', 1, 1),
            ('Nihari', 'Slow-cooked beef shank stew with spicy marrow gravy.', 19.99, 'Non-Veg Curries', 'https://untoldrecipesbynosheen.com/wp-content/uploads/2020/09/Nihari-new-hero-scaled.jpeg', 0, 1),
            ('Chicken Jalfrezi', 'Boneless chicken stir-fried with peppers.', 16.99, 'Non-Veg Curries', 'https://www.daringgourmet.com/wp-content/uploads/2024/05/Chicken-Jalfrezi-Recipe-25.jpg', 0, 1),
            ('Beef Achari Gosht', 'Beef cooked with pickling spices and green chilies.', 18.99, 'Non-Veg Curries', 'https://www.flourandspiceblog.com/wp-content/uploads/2023/01/IMG_0310-360x360.jpg', 0, 1),

            # BIRYANI
            ('Signature Mutton Biryani', 'Aromatic rice layered with tender goat meat.', 18.99, 'Biryani', 'https://salasdaily.com/cdn/shop/files/signaturebiryani.jpg?v=1714714705', 1, 1),
            ('Chicken Dum Biryani', 'Hyderabadi style slow-cooked chicken and rice.', 16.99, 'Biryani', 'https://static.toiimg.com/thumb/54308405.cms?imgsize=510571&width=800&height=800', 0, 1),
            ('Shrimp Biryani', 'Zesty shrimp cooked with fragrant basmati.', 19.99, 'Biryani', 'https://www.cubesnjuliennes.com/wp-content/uploads/2020/12/Prawn-Biryani-Recipe.jpg', 0, 1),
            ('Beef Biryani', 'Robust beef chunks layered with spicy saffron rice.', 17.99, 'Biryani', 'https://t4.ftcdn.net/jpg/18/88/44/23/360_F_1888442305_X7yWY1cE418zVwA8uOoOe7R1PJII79nl.jpg', 0, 1),
            ('Egg Biryani', 'Hard-boiled eggs tossed in a spicy biryani masala.', 14.99, 'Biryani', 'https://spicecravings.com/wp-content/uploads/2020/10/Egg-Biryani-Featured-1.jpg', 0, 1),
            ('Vegetable Dum Biryani', 'Seasonal vegetables steamed with aromatic rice.', 13.99, 'Biryani', 'https://www.cookingcarnival.com/wp-content/uploads/2025/09/Vegetable-Dum-Biryani-5.jpg', 0, 1),

            # BREADS
            ('Garlic Naan', 'Tandoori bread with garlic and butter.', 3.99, 'Breads', 'https://somebodyfeedseb.com/wp-content/uploads/2024/04/Square-2024.03.23-Cheese-garlic-naan-2444.jpg', 0, 1),
            ('Roti', 'Whole wheat flatbread baked in a clay oven.', 2.99, 'Breads', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTmBLC4uzokC_lXtxXTs_Nw2NnAsLI6iiW5hg&s', 0, 1),
            ('Cheese Naan', 'Naan stuffed with melted mozzarella and herbs.', 5.99, 'Breads', 'https://therecipespk.com/wp-content/uploads/2017/10/Cheese-Naan.jpg', 0, 1),
            ('Lacha Paratha', 'Multi-layered crispy bread fried with ghee.', 4.99, 'Breads', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQtzwvbPp5689HfM4SlWDSET42G51Iy6utPOQ&s', 0, 1),

            # DESSERTS
            ('Gulab Jamun', 'Warm dumplings in cardamom sugar syrup.', 6.99, 'Desserts', 'https://www.cadburydessertscorner.com/hubfs/dc-website-2022/articles/soft-gulab-jamun-recipe-for-raksha-bandhan-from-dough-to-syrup-all-you-need-to-know/soft-gulab-jamun-recipe-for-raksha-bandhan-from-dough-to-syrup-all-you-need-to-know.webp', 0, 1),
            ('Pistachio Kheer', 'Slow-cooked rice pudding topped with nuts.', 7.99, 'Desserts', 'https://cdn-food.tribune.com.pk/gallery/vKQOY9v3o1sqTMc59yusPjV6zNbpy35Dxnf7JK5y.jpeg', 0, 1),
            ('Ras Malai', 'Soft paneer discs chilled in thickened saffron milk.', 8.99, 'Desserts', 'https://eatsbyramya.com/wp-content/uploads/2024/10/rasmalai_can_recipe.jpg', 0, 1),
            ('Carrot Pudding', 'Traditional carrot halwa with khoya and nuts.', 9.99, 'Desserts', 'https://butteroverbae.com/wp-content/uploads/2018/12/gajar-ka-halwa-1.jpg', 1, 1),

            # BEVERAGES & DRINKS
            ('Mango Lassi', 'Creamy yogurt drink blended with sweet mangoes.', 5.99, 'Beverages & Drinks', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlSlQ45vH_JReiUTNXyYvVMwW6Lb5G05fLRA&s', 1, 1),
            ('Sweet Lassi', 'Chilled yogurt drink with a hint of cardamom.', 4.99, 'Beverages & Drinks', 'https://www.indianveggiedelight.com/wp-content/uploads/2023/01/sweet-lassi-recipe-featured.jpg', 0, 1),
            ('Fresh Lime Soda', 'Refreshing lime juice with soda and salt/sugar.', 3.99, 'Beverages & Drinks', 'https://thumbs.dreamstime.com/b/refreshing-lime-soda-ice-cubes-limes-vibrant-glass-brimming-fresh-slices-sits-rustic-wooden-table-summer-386648343.jpg', 0, 1),
            ('Masala Chai', 'Aromatic spiced tea brewed with milk and ginger.', 2.99, 'Beverages & Drinks', 'https://cdn.shopify.com/s/files/1/0758/6929/0779/files/Masala_Tea_-_Annams_Recipes_Shop_2_480x480.jpg?v=1732347934', 1, 1),
            ('Pakistani Soda', 'Assorted local sodas like Pakola.', 2.50, 'Beverages & Drinks', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQLi1IUTKLb5nfZZGE2ZU2Wv4KRB1EbpwZDjw&s', 0, 1),
            ('Kashmiri Tea', 'Traditional pink tea with pistachios and cream.', 4.99, 'Beverages & Drinks', 'https://www.chilitochoc.com/wp-content/uploads/2019/11/kashmiri-pink-chai-1-featured.jpg', 0, 1)
        ]
        conn.executemany('INSERT INTO menu (name, description, price, category, image_url, is_featured, is_available) VALUES (?, ?, ?, ?, ?, ?, ?)', expanded_items)
        conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    featured_items = conn.execute('SELECT * FROM menu WHERE is_featured = 1 AND is_available = 1 LIMIT 4').fetchall()
    conn.close()
    return render_template('index.html', items=featured_items)

@app.route('/menu')
def menu():
    conn = get_db_connection()
    # We fetch ALL items but we'll use the 'is_available' status 
    # in the HTML to show 'Sold Out' instead of hiding them completely.
    items = conn.execute('SELECT * FROM menu ORDER BY category ASC').fetchall()
    conn.close()
    return render_template('menu.html', items=items)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('password') == 'kabab2026':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_orders'))
        flash("Invalid Credentials")
    return render_template('admin_login.html')

@app.route('/admin/orders')
def admin_orders():
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM orders ORDER BY created_at DESC').fetchall()
    conn.close()
    orders = []
    for row in rows:
        order = dict(row)
        # RENAMED to order_items to fix conflict
        order['order_items'] = json.loads(row['items_json'])
        orders.append(order)
    return render_template('admin_orders.html', orders=orders)

@app.route('/admin/kitchen')
def kitchen_dashboard():
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))
    conn = get_db_connection()
    # UPDATED: Select both 'New' and 'Preparing' so they stay on the screen while cooking
    rows = conn.execute("SELECT * FROM orders WHERE status IN ('New', 'Preparing') ORDER BY created_at ASC").fetchall()
    conn.close()
    orders = []
    for row in rows:
        order = dict(row)
        order['order_items'] = json.loads(row['items_json'])
        orders.append(order)
    return render_template('kitchen_view.html', orders=orders)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        order_data = request.json
        try:
            conn = get_db_connection()
            # 1. Use a cursor so we can retrieve the ID after the insert
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO orders 
                            (customer_name, phone, items_json, total_price, payment_method) 
                            VALUES (?, ?, ?, ?, ?)''',
                         (order_data.get('name'), 
                          order_data.get('phone'), 
                          json.dumps(order_data.get('items')), 
                          order_data.get('total'),
                          order_data.get('payment_method')))
            
            # 2. Grab the auto-incremented ID of the new order
            new_order_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            
            # 3. Send that ID back to the JavaScript
            return jsonify({"status": "success", "order_id": new_order_id})
            
        except Exception as e:
            print(f"Checkout Error: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500
    return render_template('checkout.html')

# (Rest of admin/delete/update routes same as your previous code)
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin/menu')
def admin_menu():
    if not session.get('admin_logged_in'): 
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM menu').fetchall()
    conn.close()
    return render_template('admin_menu.html', items=items)

@app.route('/admin/inquiries')
def admin_inquiries():
    if not session.get('admin_logged_in'): 
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    
    # Existing data fetching
    catering = conn.execute("SELECT * FROM inquiries WHERE event_type != 'General Inquiry' ORDER BY created_at DESC").fetchall()
    general = conn.execute("SELECT * FROM inquiries WHERE event_type = 'General Inquiry' ORDER BY created_at DESC").fetchall()
    
    # New Stats Logic
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    stats = {
    'new_leads': conn.execute("SELECT COUNT(*) FROM inquiries WHERE created_at >= ?", (seven_days_ago,)).fetchone()[0],
    'pending': conn.execute("SELECT COUNT(*) FROM inquiries WHERE status = 'Pending'").fetchone()[0],
    'total_guests': conn.execute("SELECT SUM(guest_count) FROM inquiries WHERE event_type != 'General Inquiry'").fetchone()[0] or 0,
    # New line below to sum up the cash flow
    'total_revenue': conn.execute("SELECT SUM(estimated_revenue) FROM inquiries").fetchone()[0] or 0
}
    
    conn.close()
    return render_template('admin_inquiries.html', catering=catering, general=general, stats=stats)

@app.route('/admin/order/update/<int:id>/<string:new_status>', methods=['POST'])
def update_order_status(id, new_status):
    if not session.get('admin_logged_in'): 
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    conn.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, id))
    conn.commit()
    conn.close()
    
    flash(f"Order #{id} updated to {new_status}")
    return redirect(request.referrer or url_for('admin_orders'))

@app.route('/admin/order/delete/<int:id>', methods=['POST'])
def delete_order(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM orders WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_orders'))

@app.route('/order-success')
def order_success():
    return render_template('order_success.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/catering')
def catering():
    return render_template('catering.html')

@app.route('/submit_inquiry', methods=['POST'])
def submit_inquiry():
    # 1. YOU MUST EXTRACT THESE FIRST
    name = request.form.get('name')
    email = request.form.get('email')
    event_type = request.form.get('event_type', 'General Inquiry')
    event_date = request.form.get('event_date')
    message = request.form.get('message')
    
    # 2. Handle the numeric data
    raw_guests = request.form.get('guest_count')
    guest_count = int(raw_guests) if raw_guests and raw_guests.isdigit() else 0
    
    # 3. Calculate revenue
    estimated_revenue = guest_count * 50 

    # 4. Save to Database
    conn = get_db_connection()
    conn.execute('''INSERT INTO inquiries (name, email, event_type, guest_count, 
                    event_date, message, estimated_revenue) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                 (name, email, event_type, guest_count, event_date, message, estimated_revenue))
    conn.commit()
    conn.close()
    
    flash("Your vision has been received. Our event specialist will be in touch.")
    return redirect(request.referrer or url_for('index'))

@app.route('/track/<int:order_id>')
def track_order(order_id):
    conn = get_db_connection()
    order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    conn.close()
    
    if order is None:
        flash("Order not found.")
        return redirect(url_for('index'))
        
    # Convert to dict and parse the JSON items so we can list them
    order_data = dict(order)
    order_data['items'] = json.loads(order['items_json'])
    
    return render_template('track.html', order=order_data)

@app.route('/admin/menu/update/<int:id>', methods=['POST'])
def update_menu_item(id):
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))
    
    name = request.form.get('name')
    price = request.form.get('price')
    # If category is missing from form, we'll default to 'Uncategorized' so it doesn't crash
    category = request.form.get('category') or 'Uncategorized'
    
    avail = 1 if request.form.get('is_available') else 0
    feat = 1 if request.form.get('is_featured') else 0
    
    conn = get_db_connection()
    conn.execute('UPDATE menu SET name=?, price=?, category=?, is_available=?, is_featured=? WHERE id=?', 
                 (name, price, category, avail, feat, id))
    conn.commit()
    conn.close()
    flash(f"Updated {name}")
    return redirect(url_for('admin_menu'))

@app.route('/admin/menu/delete/<int:id>', methods=['POST'])
def delete_menu_item(id):
    if not session.get('admin_logged_in'): return redirect(url_for('admin_login'))
    conn = get_db_connection()
    conn.execute('DELETE FROM menu WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash("Item deleted")
    return redirect(url_for('admin_menu'))

@app.route('/admin/inquiry/toggle/<int:id>', methods=['POST'])
def toggle_status(id):
    if not session.get('admin_logged_in'): 
        return jsonify({"error": "Unauthorized"}), 401
    
    conn = get_db_connection()
    inquiry = conn.execute('SELECT status FROM inquiries WHERE id = ?', (id,)).fetchone()
    
    if inquiry:
        new_status = 'Contacted' if inquiry['status'] == 'Pending' else 'Pending'
        conn.execute('UPDATE inquiries SET status = ? WHERE id = ?', (new_status, id))
        conn.commit()
    conn.close()

    # If the request comes from an AJAX/Fetch call, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
        return jsonify({"status": "success", "new_status": new_status})
    
    # Otherwise, redirect as usual
    return redirect(url_for('admin_inquiries'))

@app.route('/admin/inquiry/delete/<int:id>', methods=['POST'])
def delete_inquiry(id):
    if not session.get('admin_logged_in'): 
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    conn.execute('DELETE FROM inquiries WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash("Inquiry archived successfully.")
    return redirect(url_for('admin_inquiries'))

def migrate_db():
    conn = get_db_connection()
    try:
        # This adds the column only if it doesn't exist
        conn.execute("ALTER TABLE inquiries ADD COLUMN estimated_revenue REAL DEFAULT 0")
        conn.commit()
        print("Migration: estimated_revenue column added.")
    except sqlite3.OperationalError:
        print("Migration: Column already exists, skipping.")
    conn.close()

if __name__ == "__main__":
    init_db()
    migrate_db() # Run the migration right after init
    app.run(debug=True, port=5001)