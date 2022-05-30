from multiprocessing import connection
import sqlite3

def add_item(ja_name, en_name, category_id, image_hash):
    connection = sqlite3.connect("../db/mercari.sqlite3")
    cursor = connection.cursor()
    image = image_hash + ".jpg"
    cursor.execute("""
    INSERT INTO items (ja_name, en_name, category_id, image_filename)
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
    ON items.category_id = category.id
    """)
    items = cursor.fetchall()
    connection.close()
    return items


def get_item(item_id):
    connection = sqlite3.connect("../db/mercari.sqlite3")
    cursor = connection.cursor()
    cursor.execute("""
    SELECT items.id, items.en_name, items.ja_name, category.name AS category_name, items.image_filename
    FROM items
    LEFT JOIN category
    ON items.category_id = category.id
    WHERE items.id = ?
    """, (item_id,))
    item = cursor.fetchone()
    connection.close()
    return item


def search_items(keyword):
    connection = sqlite3.connect("../db/mercari.sqlite3")
    cursor = connection.cursor()
    cursor.execute("""
    SELECT items.id, items.ja_name, items.en_name, category.name AS category_name, items.image_filename
    FROM items
    LEFT JOIN category
    ON items.category_id = category.id
    WHERE items.en_name LIKE ? OR items.ja_name LIKE ?
    """, ("%" + keyword + "%", "%" + keyword + "%"))
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
