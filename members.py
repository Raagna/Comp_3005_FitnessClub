import psycopg2
from datetime import datetime, timedelta

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
        cursor.execute("SELECT routine FROM routines JOIN member_routines ON routines.routine_id = member_routines.routine_id WHERE member_id = %s", (member_id,))
        exercise_routines = cursor.fetchall()
        print("Exercise Routines:")
        exercises = ""
        for row in exercise_routines:
            for exercise in row:
                exercise = exercise.strip()
                exercises += f'{exercise}, ' 
        if exercises == "":
            print('No Favorite Exercises added')
        else:   
            print(exercises)
    
        
        # Displaying fitness achievements1
        cursor.execute("SELECT max_deadlift_kg, max_benchpress_kg, weight_kg FROM members WHERE member_id = %s", (member_id,))
        member_profile = cursor.fetchone()
        print("\nFitness Achievements:")
        print(f"Your Max Deadlift Is: {member_profile[0]}kg")
        print(f"Your Max Benchpress Is: {member_profile[1]}kg")
        print(f"Your Current Weight Is: {member_profile[2]}kg")
        # Displaying health statistics
        cursor.execute("SELECT weight_kg, height_cm FROM members WHERE member_id = %s", (member_id,))
        health_statistics = cursor.fetchone()
        print("\nHealth Statistics:")
        print(f"Your Current Weight Is: {health_statistics[0]}kg")
        print(f'Your Current Height Is: {health_statistics[1]}cm')
        
        choice = input('Would you like to add exercises? (y/n): ')
        if choice.upper() == 'Y' or choice.upper() == 'YES':
            new_exercise = input("Add exercise (type 'quit' to stop): ")
            add_exercise(new_exercise,member_id)
            while new_exercise.upper() != 'QUIT':
                new_exercise = input("Add exercise (type 'quit' to stop): ")
                add_exercise(new_exercise,member_id)
        cursor.close()
        conn.close()
    except Exception as e:
        print("Error:", e)

def book_session(member_id):

    conn = get_db_connection()
    cursor = conn.cursor()
        
    trainer_name = input("Enter trainer name: ")

    # Prompt for session date
    session_date = input("Enter session day: ")

    # Prompt for session time
    session_time_str = input("Enter session time (HH:MM) (Times are 30 minute intervals): ")
    session_time = datetime.strptime(session_time_str, "%H:%M").time()
    hour, minute = divmod(session_time.minute + 15, 30)
    session_time.replace(hour=session_time.hour + hour, minute=minute * 30 % 60)
    # rounds to the nearest 30 minute
    
    # Check if trainer exists
    cursor.execute("SELECT trainer_id FROM trainers WHERE trainer_name = %s", (trainer_name,))
    trainer = cursor.fetchone()
    if not trainer:
        print("Trainer not found.")
        return

    trainer_id = trainer[0]
    
    # Check if trainer is available at the specified time and date
    cursor.execute("""
        SELECT slot_id
        FROM availability_slots
        WHERE trainer_id = %s
        AND day_of_week = %s
        AND start_time <= %s
        AND end_time >= %s
        """, (trainer_id, session_date, session_time, session_time))
    available_slots = cursor.fetchall()

    if not available_slots:
        print("Trainer is not available at the specified time and date.")
        return

    # Book the session
    slot_id = available_slots[0][0]  # Assuming the first available slot is booked
    cursor.execute("INSERT INTO session_members (slot_id, member_id) VALUES (%s, %s)", (slot_id, member_id))
    conn.commit()
    print("Individual session successfully booked!")
        
def schedule_session(member_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Check if the member has any existing sessions booked
        cursor.execute("SELECT slot_id FROM session_members WHERE member_id = %s", (member_id,))
        existing_sessions = cursor.fetchall()
        
        if existing_sessions:
            choice = input("Would you like to reschedule or cancel your existing session? or book another session? (reschedule/cancel/book): ")
            
            if choice.lower() == "reschedule":
                # Reschedule session
                reschedule_session(member_id)
                return
            elif choice.lower() == "cancel":
                # Cancel session
                cancel_session(member_id)
                return
            elif choice.lower() == "book":
                # book session
                book_session(member_id)
                return
            else:
                print("Invalid choice.")
                return
        else:
            book_session(member_id)
    except psycopg2.Error as e:
        print("Error booking individual session:", e)

    finally:
        if conn:
            conn.close()  
        
        
def reschedule_session(member_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
         # Prompt for session details
        trainer_name = input("Enter current trainer name: ")
        session_date = input("Enter current session day: ")
        session_time_str = input("Enter current session time (HH:MM): ")
        session_time = datetime.strptime(session_time_str, "%H:%M").time()
        
        # Find session based on provided details
        cursor.execute("""
            SELECT av.slot_id
            FROM session_members sm
            JOIN availability_slots av ON sm.slot_id = av.slot_id
            JOIN trainers t ON av.trainer_id = t.trainer_id
            WHERE sm.member_id = %s
            AND t.trainer_name = %s
            AND av.day_of_week = %s
            AND av.start_time = %s
            AND av.end_time = %s
            """, (member_id, trainer_name, session_date, session_time, session_time))
        session = cursor.fetchone()
        
        if not session:
            print("Session not found. Please check your input.")
            return
        
        new_trainer_name = input("Enter new trainer name: ")
        new_session_date = input("Enter new session day: ")
        new_session_time_str = input("Enter new session time (HH:MM): ")
        new_session_time = datetime.strptime(new_session_time_str, "%H:%M").time()
        
        # Check if the new slot is available
        cursor.execute("""
            SELECT availability_slots.slot_id 
            FROM availability_slots 
            JOIN trainers ON availability_slots.trainer_id = trainers.trainer_id 
            WHERE trainers.trainer_name = %s 
            AND day_of_week = %s 
            AND start_time <= %s 
            AND end_time >= %s
            """, (new_trainer_name, new_session_date.strftime("%A"), new_session_time, new_session_time))
       
        new_session = cursor.fetchone()
        if new_session:
            print("Trainer is not available at the specified time and date.")
            return

        # Update the session details for the member
        cursor.execute("""
            UPDATE session_members 
            SET slot_id = %s, date = %s, time = %s
            WHERE member_id = %s AND date = %s AND time = %s
            """, (new_session[0], new_session_date, new_session_time, member_id, session_date, session_time))
        conn.commit()
        print("Session successfully rescheduled.")

    except psycopg2.Error as e:
        print("Error rescheduling session:", e)

    finally:
        if conn:
            conn.close()

        
        
        
def cancel_session(member_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Prompt for session details to cancel
        session_date = input("Enter the session day to cancel: ")
        session_time_str = input("Enter the session time to cancel (HH:MM): ")
        session_time = datetime.strptime(session_time_str, "%H:%M").time()

      # Check if the session exists for the member
        cursor.execute("""
            DELETE FROM session_members 
            WHERE member_id = %s 
            AND slot_id IN (
                SELECT slot_id 
                FROM session_members 
                JOIN availability_slots ON availability_slots.slot_id = session_members.slot_id
                WHERE member_id = %s 
                AND date = %s 
                AND start_time = %s
            )
            """, (member_id, member_id, session_date, session_time))
        conn.commit()
        print("Session successfully canceled.")

    except psycopg2.Error as e:
        print("Error canceling session:", e)

    finally:
        if conn:
            conn.close() 
            
            
            
            
        
            
            
            
            
def add_exercise(exercise, member_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO routines (routine) VALUES (%s) RETURNING routine_id", (exercise,))
        exercise_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO member_routines (member_id, routine_id) VALUES (%s, %s)", (member_id, exercise_id))
        
        conn.commit()
        cursor.close()
        conn.close()
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
        # print("Error:", error)
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

