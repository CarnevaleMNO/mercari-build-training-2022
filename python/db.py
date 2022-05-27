from multiprocessing import connection
import sqlite3


def add_item(ja_name, en_name, category_id, image_hash):
    connection = sqlite3.connect("../db/mercari.sqlite3")
    cursor = connection.cursor()
    image = image_hash + ".jpg"
    cursor.execute("""
    INSERT INTO items (ja_name, en_name, category, image_filename)
    VALUES (?, ?, ?, ?)
    """, (ja_name, en_name, category_id, image))
    connection.commit()
    connection.close()


def get_items():
    connection = sqlite3.connect("../db/mercari.sqlite3")
    cursor = connection.cursor()
    cursor.execute("""
    SELECT items.id, items.ja_name, items.en_name, category.name AS category_name, items.image_filename
    FROM items
    LEFT JOIN category
    ON items.category = category.id
    """)
    items = cursor.fetchall()
    connection.close()
    return items


def get_item(item_id):
    connection = sqlite3.connect("../db/mercari.sqlite3")
    cursor = connection.cursor()
    cursor.execute("""
    SELECT items.id, items.name, category.name AS category_name, items.image_filename
    FROM items
    LEFT JOIN category
    ON items.category = category.id
    WHERE items.id = ?
    """, (item_id,))
    item = cursor.fetchone()
    connection.close()
    return item


def search_items(keyword):
    connection = sqlite3.connect("../db/mercari.sqlite3")
    cursor = connection.cursor()
    cursor.execute("""
    SELECT items.id, items.name, items.category, category.name AS category_name, items.image_filename
    FROM items
    LEFT JOIN category
    ON items.category = category.id
    WHERE items.name LIKE ?
    """, ("%" + keyword + "%",))
    items = cursor.fetchall()
    connection.close()
    return items


def delete_item(item_id):
    connection = sqlite3.connect("../db/mercari.sqlite3")
    cursor = connection.cursor()
    cursor.execute("""
    DELETE FROM items
    WHERE id = ?
    """, (item_id,))
    connection.commit()
    connection.close()

#create items table

# connection = sqlite3.connect("../db/mercari.sqlite3")
# cursor = connection.cursor()
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS items (
#     id INTEGER PRIMARY KEY,
#     ja_name TEXT,
#     en_name TEXT,
#     category INTEGER,
#     image_filename TEXT
# )
# """)

# create category table

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS category (
#     id INTEGER PRIMARY KEY,
#     name TEXT
# )
# """)
# connection.commit()
# connection.close()