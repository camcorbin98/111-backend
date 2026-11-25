from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DB_NAME = "online-store.db"


# ---------------- TABLES ----------------

def init_db():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coupons (
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

    connection.commit()
    connection.close()


# ---------------- HEALTH ----------------

@app.get("/health")
def health_check():
    return jsonify({"status": "ok"})


# ---------------- COUPONS ----------------

# POST /api/coupons
@app.post("/api/coupons")
def create_coupon():
    new_coupon = request.get_json()
    code = new_coupon["code"]
    discount = new_coupon["discount"]

    if discount > 90:
        return jsonify({
            "success": False,
            "message": "Invalid coupon discount"
        }), 400

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO coupons (code, discount)
            VALUES (?, ?)
        """, (code, discount))
        connection.commit()
    except sqlite3.IntegrityError:
        return jsonify({
            "success": False,
            "message": "Coupon code already exists"
        }), 400
    finally:
        connection.close()

    return jsonify({
        "success": True,
        "message": "Coupon created successfully"
    }), 201


# GET /api/coupons
@app.get("/api/coupons")
def get_coupons():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM coupons")
    coupons_db = cursor.fetchall()
    connection.close()

    coupons_list = []

    for coupon in coupons_db:
        coupons_list.append(dict(coupon))

    return jsonify({
        "success": True,
        "message": "Coupons retrieved successfully",
        "data": coupons_list
    }), 200


# GET /api/coupons/<id>
@app.get("/api/coupons/<int:coupon_id>")
def get_coupon_by_id(coupon_id):
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM coupons WHERE id = ?",
        (coupon_id,)
    )

    coupon_db = cursor.fetchone()
    connection.close()

    if coupon_db is None:
        return jsonify({
            "success": False,
            "message": "Coupon not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Coupon retrieved successfully",
        "data": dict(coupon_db)
    }), 200


# DELETE /api/coupons/<id>
@app.delete("/api/coupons/<int:coupon_id>")
def delete_coupon_by_id(coupon_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM coupons WHERE id = ?",
        (coupon_id,)
    )

    coupon_db = cursor.fetchone()

    if not coupon_db:
        connection.close()
        return jsonify({
            "success": False,
            "message": "Coupon not found"
        }), 404

    cursor.execute(
        "DELETE FROM coupons WHERE id = ?",
        (coupon_id,)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Coupon deleted successfully"
    }), 200


# PUT /api/coupons/<id>
@app.put("/api/coupons/<int:coupon_id>")
def update_coupon_by_id(coupon_id):
    updated_coupon = request.get_json()
    code = updated_coupon["code"]
    discount = updated_coupon["discount"]

    if discount > 90:
        return jsonify({
            "success": False,
            "message": "Invalid coupon discount"
        }), 400

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM coupons WHERE id = ?",
        (coupon_id,)
    )

    coupon_db = cursor.fetchone()

    if not coupon_db:
        connection.close()
        return jsonify({
            "success": False,
            "message": "Coupon not found"
        }), 404

    try:
        cursor.execute("""
            UPDATE coupons
            SET code = ?, discount = ?
            WHERE id = ?
        """, (code, discount, coupon_id))

        connection.commit()
    except sqlite3.IntegrityError:
        return jsonify({
            "success": False,
            "message": "Coupon code already exists"
        }), 400
    finally:
        connection.close()

    return jsonify({
        "success": True,
        "message": "Coupon updated successfully"
    }), 200


# ---------------- PRODUCTS ----------------

categories = ["electronics", "education", "food"]


# POST /api/products
@app.post("/api/products")
def create_product():
    new_product = request.get_json()
    name = new_product["name"]
    price = new_product["price"]
    category = new_product["category"]
    image = new_product["image"]

    if category not in categories:
        return jsonify({
            "success": False,
            "message": "Invalid category"
        }), 400

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO products (name, price, category, image)
            VALUES (?, ?, ?, ?)
        """, (name, price, category, image))

        connection.commit()
    except sqlite3.IntegrityError:
        return jsonify({
            "success": False,
            "message": "Product name already exists"
        }), 400
    finally:
        connection.close()

    return jsonify({
        "success": True,
        "message": "Product created successfully"
    }), 201


# GET /api/products
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
        products_list.append(dict(product))

    return jsonify({
        "success": True,
        "message": "Products retrieved successfully",
        "data": products_list
    }), 200


# GET /api/products/<id>
@app.get("/api/products/<int:product_id>")
def get_product_by_id(product_id):
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    )

    product_db = cursor.fetchone()
    connection.close()

    if product_db is None:
        return jsonify({
            "success": False,
            "message": "Product not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Product retrieved successfully",
        "data": dict(product_db)
    }), 200


# PUT /api/products/<id>
@app.put("/api/products/<int:product_id>")
def update_product_by_id(product_id):
    updated_product = request.get_json()

    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    )

    product_db = cursor.fetchone()

    if product_db is None:
        connection.close()
        return jsonify({
            "success": False,
            "message": "Product not found"
        }), 404

    name = updated_product.get("name", product_db["name"])
    price = updated_product.get("price", product_db["price"])
    category = updated_product.get("category", product_db["category"])
    image = updated_product.get("image", product_db["image"])

    if category not in categories:
        connection.close()
        return jsonify({
            "success": False,
            "message": "Invalid category"
        }), 400

    try:
        cursor.execute("""
            UPDATE products
            SET name = ?, price = ?, category = ?, image = ?
            WHERE id = ?
        """, (name, price, category, image, product_id))

        connection.commit()
    except sqlite3.IntegrityError:
        return jsonify({
            "success": False,
            "message": "Invalid product data or duplicate name"
        }), 400
    finally:
        connection.close()

    return jsonify({
        "success": True,
        "message": "Product updated successfully"
    }), 200


# DELETE /api/products/<id>
@app.delete("/api/products/<int:product_id>")
def delete_product_by_id(product_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    )

    product_db = cursor.fetchone()

    if product_db is None:
        connection.close()
        return jsonify({
            "success": False,
            "message": "Product not found"
        }), 404

    cursor.execute(
        "DELETE FROM products WHERE id = ?",
        (product_id,)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Product deleted successfully"
    }), 200


# ---------------- RUN APPLICATION ----------------

init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5001)


