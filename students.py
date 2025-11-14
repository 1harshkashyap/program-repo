import mysql.connector

# Database connection details
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_mysql_username',
    'password': 'your_mysql_password',
    'database': 'student_db'
}

def create_connection():
    """Establishes a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_table(conn):
    """Creates the 'students' table if it doesn't exist."""
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INT,
                grade VARCHAR(50)
            )
        """)
        conn.commit()
        print("Table 'students' ensured to exist.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        cursor.close()

def add_student(conn, name, age, grade):
    """Adds a new student record to the database."""
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)"
        values = (name, age, grade)
        cursor.execute(sql, values)
        conn.commit()
        print(f"Student '{name}' added successfully.")
    except mysql.connector.Error as err:
        print(f"Error adding student: {err}")
    finally:
        cursor.close()

def view_students(conn):
    """Retrieves and displays all student records."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        if students:
            print("\n--- Student Records ---")
            for student in students:
                print(f"ID: {student[0]}, Name: {student[1]}, Age: {student[2]}, Grade: {student[3]}")
            print("-----------------------")
        else:
            print("No student records found.")
    except mysql.connector.Error as err:
        print(f"Error viewing students: {err}")
    finally:
        cursor.close()

def update_student(conn, student_id, new_name, new_age, new_grade):
    """Updates an existing student's details."""
    cursor = conn.cursor()
    try:
        sql = "UPDATE students SET name = %s, age = %s, grade = %s WHERE id = %s"
        values = (new_name, new_age, new_grade, student_id)
        cursor.execute(sql, values)
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Student ID {student_id} updated successfully.")
        else:
            print(f"Student ID {student_id} not found.")
    except mysql.connector.Error as err:
        print(f"Error updating student: {err}")
    finally:
        cursor.close()

def delete_student(conn, student_id):
    """Deletes a student record by ID."""
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM students WHERE id = %s"
        cursor.execute(sql, (student_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Student ID {student_id} deleted successfully.")
        else:
            print(f"Student ID {student_id} not found.")
    except mysql.connector.Error as err:
        print(f"Error deleting student: {err}")
    finally:
        cursor.close()

def main():
    conn = create_connection()
    if conn:
        create_table(conn)

        while True:
            print("\nStudent Management System Menu:")
            print("1. Add New Student")
            print("2. View All Students")
            print("3. Update Student Details")
            print("4. Delete Student")
            print("5. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                name = input("Enter student name: ")
                age = int(input("Enter student age: "))
                grade = input("Enter student grade: ")
                add_student(conn, name, age, grade)
            elif choice == '2':
                view_students(conn)
            elif choice == '3':
                student_id = int(input("Enter student ID to update: "))
                new_name = input("Enter new name: ")
                new_age = int(input("Enter new age: "))
                new_grade = input("Enter new grade: ")
                update_student(conn, student_id, new_name, new_age, new_grade)
            elif choice == '4':
                student_id = int(input("Enter student ID to delete: "))
                delete_student(conn, student_id)
            elif choice == '5':
                print("Exiting Student Management System.")
                break
            else:
                print("Invalid choice. Please try again.")
        
        conn.close()

if __name__ == "__main__":
    main()