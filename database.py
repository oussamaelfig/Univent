import sqlite3


class Database:
    def __init__(self):
        self.connection = None

    def get_connexion(self):
        if self.connection is None:
            self.connection = sqlite3.connect("database.db")
        return self.connection

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()

    def creer_new_evenement(self, creator_id, title, start_date_time,
                            end_date_time,
                            location, flyer_image_name, description):
        connect = self.get_connexion()
        cursor = connect.cursor()
        # Insert event into the database
        cursor.execute(
            "INSERT INTO Events (creator_id, title, start_date_time, "
            "end_date_time, location, flyer_image, description) VALUES (?, "
            "?, ?, ?, ?, ?, ?)",
            (
                creator_id,
                title,
                start_date_time,
                end_date_time,
                location,
                flyer_image_name,
                description,
            ),
        )
        connect.commit()
