import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pripojeni
import mysql.connector

try:
    conn = mysql.connector.connect(
        host=pripojeni.HOST,
        user=pripojeni.USER,
        password=pripojeni.PASSWORD,
        database=pripojeni.DATABASE
    )
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users67 (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS highscores67 (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            score INT NOT NULL,
            datum DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users67(id)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Tabulky users67 a highscores67 jsou v poradku.")
except mysql.connector.Error as e:
    print(f"Chyba pri pripojeni k databazi: {e}")
