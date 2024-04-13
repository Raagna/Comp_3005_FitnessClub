from datetime import datetime, timedelta

def set_trainer_availability(conn, trainer_id, day_of_week, start_time, end_time, session_length):
    # Calculate the number of slots based on session length
    start_time_obj = datetime.strptime(start_time, "%H:%M")
    end_time_obj = datetime.strptime(end_time, "%H:%M")

    num_slots = int((end_time_obj - start_time_obj).total_seconds() / (session_length * 60))

    # Connect to the database
    cursor = conn.cursor()

    # Iterate over the number of slots and add each slot to the database
    current_time = datetime.strptime(start_time, "%H:%M")
    for _ in range(num_slots):
        # Calculate the end time of the current slot
        end_slot_time = current_time + timedelta(minutes=session_length)

        # Insert the slot into the availability_slots table
        cursor.execute("""
            INSERT INTO availability_slots (trainer_id, day_of_week, start_time, end_time, availability_type)
            VALUES (%s, %s, %s, %s, 'individual')
        """, (trainer_id, day_of_week, current_time.strftime("%H:%M"), end_slot_time.strftime("%H:%M")))
        
        # Increment current_time to the start of the next slot
        current_time = end_slot_time

    # Commit changes and close the cursor and connection
    conn.commit()
    cursor.close()
    conn.close()

def search_members_by_name(conn, member_name):
    cursor = conn.cursor()

    # Search for members by name
    cursor.execute("SELECT member_id, member_name FROM members WHERE member_name ILIKE %s", ('%' + member_name + '%',))
    members = cursor.fetchall()

    # Print or return the search results
    for member_id, member_name in members:
        print(f"Member ID: {member_id}, Member Name: {member_name}")

    # Close the cursor and connection
    cursor.close()
    conn.close()
