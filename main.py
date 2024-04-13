
import psycopg2

# Database connection parameters
DB_NAME = "Comp3005_finalProject"
DB_USER = "postgres"
DB_PASSWORD = "password1"
DB_HOST = "localhost"
DB_PORT = "5432"

# Function to establish database connection
def get_db_connection():
    return psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)

# Member Functions
def register_user():
    try:
        print("User Registration:")
        member_name = input("Enter member name: ")
        username = input("Enter username: ")
        if get_user(username) is not None:
            while get_user(username) is not None:
                print("Username taken!")
                username = input("Enter username: ")
        password = input("Enter password: ")
        age = int(input("Enter age: "))
        height_cm = int(input("Enter height in cm: "))
        weight_kg = int(input("Enter weight in kg: "))
        fitness_goals = input("Enter fitness goals: ")
        goal_weight_kg = int(input("Enter goal weight in kg: "))
        max_deadlift_kg = int(input("Enter max deadlift weight in kg: "))
        goal_deadlift_kg = int(input("Enter goal deadlift weight in kg: "))
        max_benchPress_kg = int(input("Enter max bench press weight in kg: "))
        goal_benchPress_kg = int(input("Enter goal bench press weight in kg: "))

        # Set membership_status to True
        membership_status = True
        
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO members (member_name, age, membership_status,username, password, height_cm, weight_kg, fitness_goals, goal_weight_kg, 
                        max_deadlift_kg, goal_deadlift_kg, max_benchPress_kg, goal_benchPress_kg ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                       (member_name, age, membership_status, username, password, height_cm, weight_kg, fitness_goals, goal_weight_kg, max_deadlift_kg, goal_deadlift_kg, max_benchPress_kg, goal_benchPress_kg))
        conn.commit()
        cursor.close()
        conn.close()
        
        print("User registered successfully")
    except Exception as e:
        print("Error:", e)

def update_profile(member_id):
    try:
        print("Profile Management:")
        print("1. Update personal information")
        print("2. Update fitness goals")
        print("3. Update health metrics")
        choice = int(input("Enter your choice: "))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if choice == 1:
            print("1. Change name")
            print("2. Change age")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                name = input("Enter new name: ")
                cursor.execute("UPDATE members SET member_name = %s WHERE member_id = %s", (name, member_id))
            elif choice == 2:
                age = int(input("Enter new age: "))
                cursor.execute("UPDATE members SET age = %s WHERE member_id = %s", (age, member_id))
        elif choice == 2:
            fitness_goals = input("Enter new fitness goals: ")
            cursor.execute("UPDATE members SET fitness_goals = %s WHERE member_id = %s", (fitness_goals, member_id))
        elif choice == 3:
            height = int(input("Enter height in cm: "))
            weight = int(input("Enter weight in kg: "))
            cursor.execute("UPDATE members SET height_cm = %s AND SET weight_kg = %s VALUES (%s, %s)", (height, weight))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("Profile updated successfully")
    except Exception as e:
        print("Error:", e)

def display_dashboard(member_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Displaying exercise routines
        cursor.execute("SELECT * FROM routines")
        exercise_routines = cursor.fetchall()
        print("Exercise Routines:")
        for routine in exercise_routines:
            print(routine)
        
        # Displaying fitness achievements
        cursor.execute("SELECT * FROM members WHERE member_id = %s", (member_id,))
        member_profile = cursor.fetchone()
        print("Fitness Achievements:")
        print(member_profile)
        
        # Displaying health statistics
        cursor.execute("SELECT * FROM health_metrics WHERE member_id = %s", (member_id,))
        health_statistics = cursor.fetchone()
        print("Health Statistics:")
        print(health_statistics)
        
        cursor.close()
        conn.close()
    except Exception as e:
        print("Error:", e)
        

            
    
def schedule_session(member_id):
    try:
        print("Schedule Management:")
        trainer_id = int(input("Enter trainer ID: "))
        date = input("Enter date (YYYY-MM-DD): ")
        time = input("Enter time (HH:MM): ")
        room_id = int(input("Enter room ID: "))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if trainer is available
        cursor.execute("SELECT * FROM schedule WHERE trainer_id = %s AND date = %s AND time = %s", (trainer_id, date, time))
        if cursor.fetchone() is not None:
            print("Trainer is not available at the specified time.")
        else:
            capacity = int(input("Enter capacity: "))
            cursor.execute("INSERT INTO schedule (trainer_id, member_id, room_id, date, time, capacity) VALUES (%s, %s, %s, %s, %s, %s)", (trainer_id, member_id, room_id, date, time, capacity))
            conn.commit()
            print("Session scheduled successfully")
        
        
    except Exception as e:
        print("Error:", e)
    finally:
        if conn:
            cursor.close()
            conn.close()
            

# Trainer Functions
def set_trainer_availability():
    try:
        print("Trainer Schedule Management:")
        trainer_id = int(input("Enter trainer ID: "))
        date = input("Enter date (YYYY-MM-DD): ")
        start_time = input("Enter start time (HH:MM): ")
        end_time = input("Enter end time (HH:MM): ")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO trainer_availability (trainer_id, date, start_time, end_time) VALUES (%s, %s, %s, %s)", (trainer_id, date, start_time, end_time))
        conn.commit()
        cursor.close()
        conn.close()
        
        print("Trainer availability set successfully")
    except Exception as e:
        print("Error:", e)

def search_member_profile():
    try:
        member_name = input("Enter member's name: ")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members WHERE member_name LIKE %s", ('%' + member_name + '%',))
        member_profiles = cursor.fetchall()
        cursor.close()
        conn.close()
        
        print("Member Profiles:")
        for profile in member_profiles:
            print(profile)
    except Exception as e:
        print("Error:", e)
        
        
def get_member_id(username, password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT member_id FROM members WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except (Exception, psycopg2.Error) as error:
        print("Error:", error)
        return None
    finally:
        if conn:
            cursor.close()
            conn.close()
            
            
            
def get_user(user):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT member_id FROM members WHERE username = %s", (user))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
        
    except (Exception, psycopg2.Error) as error:
        print("Error:", error)
        return None
    finally:
        if conn:
            cursor.close()
            conn.close()    
def get_most_recent_member_id():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        
        cursor.execute("SELECT MAX(member_id) FROM members")
        
        result = cursor.fetchone()
        
        if result:
            return result[0]
        else:
            return None
        
    except (Exception, psycopg2.Error) as error:
        print("Error:", error)
        return None
    
    finally:
        if conn:
            cursor.close()
            conn.close()



# Main function
def main():
    try:
        while True:
            print("\nSelect User Type:")
            print("1. Member")
            print("2. Trainer")
            print("3. Exit")
            user_type = int(input("Enter your choice: "))

            if user_type == 1:
                choice = int(input("Would you like to \n 1. Log in \n or \n 2. Register as a member?: "))
                if choice == 1:
                    user = input("Enter member username: ")
                    password = input("Enter member password: ")
                    member_id = get_member_id(user,password)
                    if member_id is None:
                        while member_id is None:
                            print("Incorrect Username or password!")
                            user = input("Enter member Username: ")
                            password = input("Enter member Password: ")
                            member_id = get_member_id(user,password)
                else: 
                    register_user()
                    member_id = get_most_recent_member_id();
                    
                print("\nMember Functions:")
                print("1. Profile Management")
                print("2. Dashboard Display")
                print("3. Schedule Management")
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    update_profile(member_id)
                elif choice == 2:
                    display_dashboard(member_id)
                elif choice == 3:
                    schedule_session(member_id)        
                else:
                    print("Invalid choice. Please try again.")

            elif user_type == 2:
                print("\nTrainer Functions:")
                print("1. Set Trainer Availability")
                print("2. Search Member Profile")
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    set_trainer_availability()
                elif choice == 2:
                    search_member_profile()
                else:
                    print("Invalid choice. Please try again.")

            elif user_type == 3:
                break

            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    main()