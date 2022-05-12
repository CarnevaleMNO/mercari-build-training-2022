import sqlite3
import os

# # Create a table
# connection = sqlite3.connect('db/mercari.sqlite3')
# cursor = connection.cursor()

# cursor.execute(""" CREATE TABLE IF NOT EXISTS items (
#     id INTEGER PRIMARY KEY,
#     name TEXT,
#     category_id INTEGER,
#     image TEXT)""")
# # create category table
# cursor.execute(""" CREATE TABLE IF NOT EXISTS category (
#     id INTEGER PRIMARY KEY,
#     name TEXT)""")

# connection.commit() # Commit the changes
# connection.close() # Close the connection

# combine tables

def show_items():
    all_items = {"items": []}
    connection = sqlite3.connect('db/mercari.sqlite3')
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM items INNER JOIN category ON items.category_id = category.id")
    for row in cursor.fetchall():
        all_items["items"].append(
            {"id": row[0], "name": row[1], "category": row[5], "image": row[3]})
    connection.close()
    return all_items


def search_items(keyword):
    all_items = {"items": []}
    connection = sqlite3.connect('db/mercari.sqlite3')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM items WHERE name LIKE ?",
                   ("%" + keyword + "%",))
    for row in cursor.fetchall():
        all_items["items"].append(
            {"id": row[0], "name": row[1], "category": row[2]})
    connection.close()
    return all_items


def get_item(id):
    item = {}
    connection = sqlite3.connect('db/mercari.sqlite3')
    cursor = connection.cursor()
    # combine tables
    cursor.execute(
        "SELECT * FROM items INNER JOIN category ON items.category_id = category.id WHERE items.id = ?", (id,))
    for row in cursor.fetchall():
        item = {"id": row[0], "name": row[1],
                "category": row[5], "image": row[3]}
    connection.close()
    return item


def create_item(name, category_id, image_hash):
    connection = sqlite3.connect('db/mercari.sqlite3')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO items (name, category_id, image) VALUES (?, ?, ?)",
                     (name, category_id, image_hash))
    connection.commit()
    connection.close()


def delete_item(id):
    connection = sqlite3.connect('db/mercari.sqlite3')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (id,))
    connection.commit()
    connection.close()

def update_item(id, name, category_id, image):
    connection = sqlite3.connect('db/mercari.sqlite3')
    cursor = connection.cursor()
    cursor.execute("UPDATE items SET name = ?, category_id = ?, image = ? WHERE id = ?",
                     (name, category_id, image, id))
    connection.commit()
    connection.close()


    
# connection = sqlite3.connect('db/mercari.sqlite3')
# cursor = connection.cursor()

# #delete table
# cursor.execute("DROP TABLE items")
# #delete item
# cursor.execute("DELETE FROM items WHERE id = ?", (1,))
# add item to category table
# cursor.execute("INSERT INTO category (name) VALUES (?)", ("Fashion",))


# connection.commit() # Commit the changes
# connection.close() # Close the connection
