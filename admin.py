def room_booking_management(conn):
    cursor = conn.cursor()

    # Select all slots
    cursor.execute("""
        SELECT slot_id, day_of_week, start_time, end_time
        FROM slots
    """)
    slots = cursor.fetchall()

    # Display the slots to the user
    print("Available Slots:")
    for idx, slot in enumerate(slots):
        slot_id, day_of_week, start_time, end_time = slot
        print(f"{idx + 1}. Slot ID: {slot_id}, Day of Week: {day_of_week}, Start Time: {start_time}, End Time: {end_time}")

    # Prompt the user to select a slot
    selected_index = int(input("Enter the index of the slot to book: ")) - 1
    selected_slot = slots[selected_index]
    slot_id = selected_slot[0]
    # Prompt the user to enter a room ID
    room_id = int(input("Enter the room ID to assign to the slot: "))

    # Check if the room ID is valid (not implemented in this example)

    # Add the booking to the schedule table
    cursor.execute("""
        INSERT INTO schedule (slot_id, room_id)
        VALUES (%s, %s)
    """, (slot_id, room_id))

    # Commit changes and close the cursor and connection
    conn.commit()
    cursor.close()
    conn.close()

def equipment_maintenance(conn):
    cursor = conn.cursor()

    # Retrieve all equipment from the equipment table
    cursor.execute("""
        SELECT * FROM equipment
    """)
    equipment_list = cursor.fetchall()

    # Display the equipment to the user
    print("Equipment List. Select any of these indices to fix broken equipment at that index, or type in 0 to return to the main menu.")
    for idx, equipment in enumerate(equipment_list):
        equipment_id, equipment_name, equipment_status = equipment
        print(f"{idx + 1}. Equipment ID: {equipment_id}, Equipment Name: {equipment_name}, Status: {equipment_status}")

    # Prompt the user to select an equipment index
    selected_index = int(input("Enter the index of the equipment to monitor: ")) - 1
    selected_equipment = equipment_list[selected_index]
    if(selected_equipment is None):
        while(selected_equipment is None):
            print("Invalid equipment ID!")
            selected_index =  int(input("Enter the index of the equipment to monitor: ")) - 1
            selected_equipment = equipment_list[selected_index]
    else:
      equipment_id = selected_equipment[0]
      equipment_status = selected_equipment[2]

    # If the status is "broken", update it to "available"
    if equipment_status == "broken":
        cursor.execute("""
            UPDATE equipment
            SET equipment_status = 'available'
            WHERE equipment_id = %s
        """, (equipment_id,))
        print(f"Equipment ID {equipment_id} status updated to 'available'.")

    # Commit changes and close the cursor and connection
    conn.commit()
    cursor.close()
    conn.close()

def class_scheduling(conn):
# Open a cursor to perform database operations
  cursor = conn.cursor()

        # Retrieve slots with availability type "group"
  cursor.execute("""SELECT slot_id, start_time, end_time FROM availability_slots WHERE availability_type = 'group'""")
  group_slots = cursor.fetchall()

        # Display group slots to the user
  print("Group Slots:")
  for slot_id, start_time, end_time in group_slots:
    print(f"Slot ID: {slot_id}, Start Time: {start_time}, End Time: {end_time}")

        # Prompt the user to select a slot ID to update
  slot_id = int(input("Enter the Slot ID to update: "))

        # Prompt the user to enter new start and end times
  new_start_time = input("Enter the new start time (HH:MM): ")
  new_end_time = input("Enter the new end time (HH:MM): ")

        # Update start and end times for the selected slot
  cursor.execute("""UPDATE availability_slots SET start_time = %s, end_time = %s WHERE slot_id = %s""", (new_start_time, new_end_time, slot_id))

  # Commit changes
  conn.commit()
  print("Group slot times updated successfully!")

def view_bill_payment(conn):
   print("Connecting to Stripe...")

   cursor = conn.cursor()

   cursor.execute("""SELECT * from bill_payment""")
   payments = cursor.fetchall()

   print("Payment info:")

   for payment in payments:
      payment_id, member_id, payment_type, payment_name = payment
      print(f"Payment ID: {payment_id}, Member ID: {member_id}, Payment Type: {payment_type}, Payment Name: {payment_name}")