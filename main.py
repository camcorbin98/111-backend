
from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DB_NAME = "online-store.db"

# ________ TABLES _________
def init_db():
    connection = sqlite3.connect(DB_NAME) #Opens a connection to the DB named 'online-stare.db'
    cursor = connection.cursor() # Create a cursor/tool that lets us send commmands (SELECT, INSERT ...)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coupons(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            discount INTEGER NOT NULL
            )
        """)


    cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                price REAL NOT NULL,
                category TEXT NOT NULL,
                image TEXT NOT NULL
            )
        """)
    connection.commit() # Save changes to the DB
    connection.close() # Close the connection to the DB

@app.get("/health")
def health_check():
    return jsonify({"status": "ok"})

# --------- COUPONS -------------
# POST /api/coupons-> create/add a coupon to the DB
@app.post("/api/coupons")
def create_coupon():
    new_coupon = request.get_json()
    code = new_coupon["code"]
    discount = new_coupon["discount"]

    connection = sqlite3.connect(DB_NAME)#Open the connection to the DB
    cursor = connection.cursor()#Create the cursor/tool work with sql commands (Insert, select)
    cursor.execute("""
                   INSERT INTO coupons (code, discount)
                   VALUES (?, ?)
    """,(code, discount))
    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Coupon created succesfully"
    }), 201 #CREATED

# GET /api/coupons -> retrieve all the coupons in the COUPONS TABLE
@app.get("/api/coupons")
def get_coupons():
    # logic here
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM coupons")
    coupons_db = cursor.fetchall() # fetchall, retrieves all the rows from the result of the query
    connection.close()

    coupons_list = []
    for coupon in coupons_db:
        print(coupon)

        coupons_list.append(dict(coupon))

    return jsonify({
        "success": True,
        "message": "Coupons retrieved successfully",
        "data": coupons_list
    }), 200

# GET /api/coupons/<2> -> Retrieve a single coupon by id using a path parameter
@app.get("/api/coupons/<int:coupon_id>")
def get_coupon_by_id(coupon_id):
    #logic here
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM coupons WHERE id = ?", (coupon_id,))
    coupon_db = cursor.fetchone()
    connection.close()

    print(coupon_db)

    if coupon_db is None:
        return jsonify({
            "success": False,
            "message": "Coupon not found"
        }), 404

    coupon = dict(coupon_db)

    return jsonify({
        "success": True,
        "message": "Coupon retrieved successfully",
        "data": coupon
    }), 200

# ------------------ PRODUCTS -----------




# POST /api/products


# GET /api/products -> return all the products from the DB


@app.get("/api/products")
def get_products():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    products_db = cursor.fetchall()
    connection.close()

    products_list = []
    for product in products_db:
        print(product)
        products_list.append(dict(product))

    return jsonify({
        "success": True,
        "message": "Products retrieved successfully",
        "data": products_list
    }), 200

#GET /api/products/<2> -> return a product by id from the DB

@app.get("/api/products/<int:product_id>")
def get_product_by_id(product_id):
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product_db = cursor.fetchone()
    connection.close()

    if product_db is None:
        return jsonify({
            "success": False,
            "message": "Product not found"
        }), 404

    product = dict(product_db)

    return jsonify({
        "success": True,
        "message": "Product retrieved successfully",
        "data": product
    }), 200



init_db() #Execute the function

if __name__ == "__main__":
    app.run(debug=True, port=5001)

