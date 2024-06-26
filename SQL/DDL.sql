
-- Table: trainers
CREATE TABLE trainers (
    trainer_id SERIAL PRIMARY KEY,
    trainer_name VARCHAR(255) NOT NULL,
    username  VARCHAR(255),
    password  VARCHAR(255)
);

-- Table: members
CREATE TABLE members (
    member_id SERIAL PRIMARY KEY,
    member_name VARCHAR(255) NOT NULL,
    username  VARCHAR(255),
    password  VARCHAR(255),
    age INTEGER,
    membership_status BOOLEAN,
    height_cm INTEGER,
    weight_kg INTEGER,
    fitness_goals VARCHAR(255),
    goal_weight_kg INTEGER,
    max_deadlift_kg INTEGER,
    goal_deadlift_kg INTEGER,
    max_benchPress_kg INTEGER,
    goal_benchPress_kg INTEGER
);

-- Table: routines
CREATE TABLE routines (
    routine_id SERIAL PRIMARY KEY,
    routine  VARCHAR(255)
);

-- Table: rooms
CREATE TABLE rooms (
    room_id SERIAL PRIMARY KEY,
    room_name  VARCHAR(255)
);

-- Table: equipment
CREATE TABLE equipment (
    equipment_id SERIAL PRIMARY KEY,
    equipment_name  VARCHAR(255),
    equipment_status  VARCHAR(255)
);

-- Table: adminStaff
CREATE TABLE adminStaff (
    staff_id SERIAL PRIMARY KEY,
    username  VARCHAR(255),
    password  VARCHAR(255),
    staff_name VARCHAR(255) NOT NULL
);

-- Table: equipment_check
CREATE TABLE equipment_check (
    staff_id INTEGER REFERENCES adminStaff(staff_id),
    equipment_id INTEGER REFERENCES equipment(equipment_id),
    PRIMARY KEY (staff_id, equipment_id)
);


-- Table: availability_slots
CREATE TABLE availability_slots (
    slot_id SERIAL PRIMARY KEY,
    trainer_id INTEGER REFERENCES trainers(trainer_id),
    day_of_week VARCHAR(255),
    start_time TIME,
    end_time TIME,
    availability_type VARCHAR(255)
);


-- Table: session_members
CREATE TABLE session_members (
    slot_id INTEGER REFERENCES availability_slots(slot_id),
    member_id INTEGER REFERENCES members(member_id),
    PRIMARY KEY (slot_id, member_id)
);

-- Table: bill_payment
CREATE TABLE bill_payment (
    member_id INTEGER REFERENCES members(member_id),
    payment VARCHAR(255),
    payment_name VARCHAR(255),
    PRIMARY KEY (member_id)
);

-- Table: member_routines
CREATE TABLE member_routines (
    member_id INTEGER REFERENCES members(member_id),
    routine_id INTEGER REFERENCES routines(routine_id),
    PRIMARY KEY (member_id, routine_id)
);

-- Table: schedule
CREATE TABLE schedule (
    slot_id INTEGER REFERENCES availability_slots(slot_id),
    room_id INTEGER REFERENCES rooms(room_id),
    PRIMARY KEY (slot_id, room_id)
);