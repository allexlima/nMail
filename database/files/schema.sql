--CREATE DATABASE n_mail ENCODING 'UTF8';
--\c n_mail;

CREATE EXTENSION citext;
CREATE EXTENSION chkpass;

CREATE TABLE n_users(
    user_id SMALLSERIAL NOT NULL,
    user_email CITEXT NOT NULL UNIQUE,
    user_name VARCHAR(50),
    user_password CHKPASS,
    user_registration_date TIMESTAMP,
    user_admin BOOL DEFAULT false,
    user_active BOOL DEFAULT true,
    PRIMARY KEY(user_id)
);

-- relationship 'have' is now 'contacts' 
-- the both foreign key fields 'c_user_id' and 'friend_id' refers to 'user_id', from 'n_users' table
-- see the EERM diagram for more details ('EERM diagram.png')
CREATE TABLE n_contacts(
    c_user_id SMALLINT NOT NULL,
    friend_id SMALLINT NOT NULL,
    friendship_start_date TIMESTAMP,
    friendship_active BOOL DEFAULT false,
    PRIMARY KEY(c_user_id, friend_id),
    FOREIGN KEY(c_user_id) REFERENCES n_users (user_id),
    FOREIGN KEY(friend_id) REFERENCES n_users (user_id)
);

CREATE TABLE n_messages(
    msg_id SMALLSERIAL NOT NULL,
    msg_title VARCHAR(90) NOT NULL,
    msg_content TEXT,
    msg_viewd BOOL DEFAULT false,
    from_system BOOL DEFAULT false,
    send_datetime TIMESTAMP,
    user_sender SMALLINT,
    user_receiver SMALLINT,
    PRIMARY KEY(msg_id),
    FOREIGN KEY(user_sender, user_receiver) REFERENCES n_contacts (c_user_id, friend_id)
);

CREATE OR REPLACE FUNCTION trg_update_friendship_date() RETURNS TRIGGER AS
    $BODY$
        BEGIN
            IF OLD.friendship_active = False AND NEW.friendship_active = True THEN
                NEW.friendship_start_date := now();
            ELSIF OLD.friendship_active = True AND NEW.friendship_active = False THEN
                NEW.friendship_start_date := NULL;
            END IF;
            RETURN NEW;
        END;
    $BODY$
LANGUAGE 'plpgsql';

CREATE TRIGGER trg_update_friendship_date
    BEFORE UPDATE ON n_contacts
    FOR EACH ROW EXECUTE PROCEDURE trg_update_friendship_date();

INSERT INTO n_users (user_email, user_name, user_password, user_registration_date, user_admin)
    VALUES ('admin@example.com', 'Admin', 'admin@123', now(), True);