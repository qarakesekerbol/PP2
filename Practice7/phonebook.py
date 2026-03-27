import csv
from connect import connect

# ---- Create Table ----
def create_table():
    conn = connect()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS contacts(
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                phone VARCHAR(50) NOT NULL UNIQUE
            );
        """)
        conn.commit()
    conn.close()

# ---- INSERT ----
def insert(name, phone):
    conn = connect()
    with conn.cursor() as cur:
        try:
            cur.execute(
                "INSERT INTO contacts(name, phone) VALUES(%s, %s)",
                (name, phone)
            )
            conn.commit()
            print(f"Added: {name} - {phone}")
        except Exception as e:
            print("Error:", e)
            conn.rollback()
    conn.close()

def insert_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    insert(name, phone)

def insert_csv(filename):
    conn = connect()
    with conn.cursor() as cur:
        try:
            with open(filename, "r") as f:
                reader = csv.reader(f)
                next(reader)  # skip header

                for row in reader:
                    if not row or len(row) < 2:
                        continue

                    name = row[0].strip()
                    phone = row[1].strip()

                    cur.execute(
                        "INSERT INTO contacts(name, phone) VALUES(%s, %s)",
                        (name, phone)
                    )

            conn.commit()
            print("CSV imported!")
        except Exception as e:
            print("Error:", e)
            conn.rollback()
    conn.close()

# ---- SELECT ----
def select_all():
    conn = connect()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM contacts")
        data = cur.fetchall()
    conn.close()
    return data

def search(pattern):
    conn = connect()
    with conn.cursor() as cur:
        like = f"%{pattern}%"
        cur.execute(
            "SELECT * FROM contacts WHERE name ILIKE %s OR phone ILIKE %s",
            (like, like)
        )
        data = cur.fetchall()
    conn.close()
    return data

# ---- UPDATE ----
def update_phone(name, phone):
    conn = connect()
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE contacts SET phone=%s WHERE name=%s",
            (phone, name)
        )
        conn.commit()
        print(f"Updated {cur.rowcount} row(s)")
    conn.close()

def update_name(phone, name):
    conn = connect()
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE contacts SET name=%s WHERE phone=%s",
            (name, phone)
        )
        conn.commit()
        print(f"Updated {cur.rowcount} row(s)")
    conn.close()

# ---- DELETE ----
def delete_name(name):
    conn = connect()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM contacts WHERE name=%s", (name,))
        conn.commit()
        print(f"Deleted {cur.rowcount} row(s)")
    conn.close()

def delete_phone(phone):
    conn = connect()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM contacts WHERE phone=%s", (phone,))
        conn.commit()
        print(f"Deleted {cur.rowcount} row(s)")
    conn.close()

# ---- PRINT ----
def print_contacts(data):
    if not data:
        print("No contacts found")
        return

    print("\n--- Contacts ---")
    for row in data:
        print(f"[{row[0]}] {row[1]} - {row[2]}")

# ---- MENU ----
def main():
    create_table()

    while True:
        print("\n---- Phonebook ----")
        print("1. Show all contacts")
        print("2. Add contact")
        print("3. Import CSV")
        print("4. Search")
        print("5. Update phone by name")
        print("6. Update name by phone")
        print("7. Delete by name")
        print("8. Delete by phone")
        print("0. Exit")

        choice = input("Choice: ")

        if choice == "1":
            print_contacts(select_all())

        elif choice == "2":
            insert_console()

        elif choice == "3":
            insert_csv("contacts.csv")

        elif choice == "4":
            pattern = input("Search: ")
            print_contacts(search(pattern))

        elif choice == "5":
            name = input("Name: ")
            phone = input("New phone: ")
            update_phone(name, phone)

        elif choice == "6":
            phone = input("Phone: ")
            name = input("New name: ")
            update_name(phone, name)

        elif choice == "7":
            name = input("Name: ")
            delete_name(name)

        elif choice == "8":
            phone = input("Phone: ")
            delete_phone(phone)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()