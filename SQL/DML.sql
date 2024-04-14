-- Insert data into the trainers table
INSERT INTO trainers (trainer_name, username, password)
VALUES ('John Doe', 'john123', 'password123'),
       ('Jane Smith', 'jane456', 'securepassword');

-- Insert data into the members table
INSERT INTO members (member_name, username, password, age, membership_status, height_cm, weight_kg, fitness_goals, goal_weight_kg, max_deadlift_kg, goal_deadlift_kg, max_benchPress_kg, goal_benchPress_kg)
VALUES ('Alice Johnson', 'alice89', 'pass123', 30, TRUE, 170, 65, 'Build muscle', 70, 100, 120, 60, 80),
       ('Bob Smith', 'bob78', 'secret321', 35, FALSE, 180, 80, 'Lose weight', 70, 80, 100, 80, 100);

-- Insert data into the routines table
INSERT INTO routines (routine)
VALUES ('Bench Press'),
       ('Dead Lift');

-- Insert data into the rooms table
INSERT INTO rooms (room_name)
VALUES ('Cardio Room'),
       ('Weight Room'),
       ('Gym Room 1'),
       ('Gym Room 2'),
       ('Gym Room 3');

-- Insert data into the equipment table
INSERT INTO equipment (equipment_name, equipment_status)
VALUES ('Treadmill', 'Broken'),
       ('Barbell', 'Available');

-- Insert data into the adminStaff table
INSERT INTO adminStaff (username, password, staff_name)
VALUES ('admin1', 'adminpass', 'ADMIN'),
       ('staff2', 'staffpass', 'Staff 2');

-- Insert data into the equipment_check table
INSERT INTO equipment_check (staff_id, equipment_id)
VALUES (1, 1),
       (2, 2);

-- Insert data into the availability_slots table
INSERT INTO availability_slots (trainer_id, day_of_week, start_time, end_time, availability_type)
VALUES (1, 'Monday', '09:00:00', '11:00:00', 'Regular'),
       (2, 'Tuesday', '10:00:00', '12:00:00', 'Regular');

-- Insert data into the session_members table
INSERT INTO session_members (slot_id, member_id)
VALUES (1, 1),
       (2, 2);

-- Insert data into the member_routines table
INSERT INTO member_routines (member_id, routine_id)
VALUES (1, 1),
       (2, 2);

-- Insert data into the bill_payment table
INSERT INTO bill_payment (member_id, staff_id, payment, payment_name)
VALUES (1, 1, '50.00', 'Membership Fee'),
       (2, 2, '75.00', 'Training Session');

-- Insert data into the schedule table
INSERT INTO schedule (slot_id, room_id)
VALUES (1, 1),
       (2, 2);