import sqlite3


class Database:
    def __init__(self):
        self.connection = None

    def get_connexion(self):
        if self.connection is None:
            self.connection = sqlite3.connect("db/database.db")
        return self.connection

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()

    #### Table users #####
    def creer_user(self, identifiant, nom, courriel, type_c, hache, salt):
        connection = self.get_connexion()
        cursor = connection.cursor()
        cursor.execute("insert into users(identifiant, nom, typeCompte, "
                       "courriel, hache, salt)"
                       "values(?,?,?,?,?,?)",
                       (identifiant, nom, type_c, courriel, hache, salt,))
        connection.commit()

    def get_user_from_iden(self, ident):
        cursor = self.get_connexion().cursor()
        cursor.execute("select identifiant from users where identifiant = ?",
                       (ident,))
        return cursor.fetchone()

    def get_user_from_courriel(self, courriel):
        cursor = self.get_connexion().cursor()
        cursor.execute("select identifiant from users where courriel = ?",
                       (courriel,))
        return cursor.fetchone()

    def get_user_pass_from_courriel(self, courriel):
        cursor = self.get_connexion().cursor()
        cursor.execute("select hache, salt, identifiant from users where "
                       "courriel = ?", (courriel,))
        return cursor.fetchone()

    def get_user_info_from_iden(self, ident):
        cursor = self.get_connexion().cursor()
        cursor.execute(
            "select nom, typeCompte, courriel from users where identifiant = ?",
            (ident,))
        return cursor.fetchone()

    #### Table sessions ####
    def creer_session(self, sessionId, userId):
        connection = self.get_connexion()
        cursor = connection.cursor()
        cursor.execute(
            "insert into sessions (identifiant, userId) values(?,?)",
            (sessionId, userId,))
        connection.commit()

    def get_id_user_from_id_session(self, id_session):
        cursor = self.get_connexion().cursor()
        cursor.execute("select userId from sessions where identifiant=?",
                       (id_session,))
        return cursor.fetchone()

    def get_session_id_from_id_session(self, id_session):
        cursor = self.get_connexion().cursor()
        cursor.execute("select identifiant from sessions where identifiant=?",
                       (id_session,))
        return cursor.fetchone()

    def get_type_compte_from_session_id(self, id_session):
        id_user = self.get_id_user_from_id_session(id_session)
        cursor = self.get_connexion().cursor()
        cursor.execute("select typeCompte from users where identifiant=?",
                       (id_user[0],))
        return cursor.fetchone()

    def delete_session(self, id_se):
        connection = self.get_connexion()
        cursor = connection.cursor()
        cursor.execute("delete from sessions where identifiant=?", (id_se,))
        connection.commit()

    #### Table events #####
    # def get_all_events(self):
    #     connect = self.get_connexion()
    #     cursor = connect.cursor()
    #     cursor.execute("SELECT * FROM events")
    #     events = cursor.fetchall()
    #
    #     return events

    def get_event_by_id(self, event_id):
        connect = self.get_connexion()
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM events WHERE event_id = ?", (event_id,))
        event = cursor.fetchone()

        return event

    def get_all_events(self, creator_id):
        connect = self.get_connexion()
        cursor = connect.cursor()
        print("this")

        # Execute SQL query to retrieve events of a specific user
        cursor.execute("SELECT * FROM Events WHERE creator_id = ?",
                       (creator_id,))
        events = cursor.fetchall()

        return events

    def creer_new_evenement(
            self,
            creator_id,
            title,
            start_date_time,
            end_date_time,
            location,
            flyer_image_blob,
            description,
            max_registration
    ):
        connect = self.get_connexion()
        cursor = connect.cursor()

        # Inserer l'evenement dans la database
        cursor.execute(
            "INSERT INTO Events (creator_id, title, start_date_time, "
            "end_date_time, location, flyer_image, description, "
            "max_registration) VALUES (?,?,?,?,?,?,?,?)",
            (
                creator_id,
                title,
                start_date_time,
                end_date_time,
                location,
                flyer_image_blob,
                description,
                max_registration
            ),
        )
        connect.commit()

        # Retourne l'ID du nouvel événement créé
        return cursor.lastrowid

    def get_event_info(self, event_id):
        conn = self.get_connexion()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT Events.*, users.nom AS creator_name 
            FROM Events 
            LEFT JOIN users ON Events.creator_id = users.identifiant 
            WHERE event_id = ?''', (event_id,))
        event_info = cursor.fetchone()

        # Convertir en dictionnaire
        col_names = [column[0] for column in cursor.description]
        event_info_dict = {col_names[index]: value for index, value in
                           enumerate(event_info)}

        return event_info_dict

    def modify_event(
            self,
            event_id,
            title,
            start_date_time,
            end_date_time,
            location,
            flyer_image,
            description,
            max_registration,
    ):
        connect = self.get_connexion()
        cursor = connect.cursor()

        # Convertit l'image en un BLOB
        flyer_image_blob = None
        if flyer_image:
            flyer_image_blob = flyer_image.read()

        # Update the event in the database using the event_id and the modified details
        cursor.execute(
            "UPDATE Events SET title = ?, start_date_time = ?, end_date_time "
            "= ?, location = ?, flyer_image = ?,"
            "description = ?, max_registration = ? WHERE event_id = ?",
            (
                title,
                start_date_time,
                end_date_time,
                location,
                flyer_image_blob,
                description,
                max_registration,
                event_id,
            ),
        )

        connect.commit()

    def delete_event(self, event_id):
        connect = self.get_connexion()
        cursor = connect.cursor()

        # Delete the event from the database using the event_id
        cursor.execute("DELETE FROM Events WHERE event_id = ?", (event_id,))

        connect.commit()

    def get_all_events_by_all_users(self):
        conn = self.get_connexion()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT Events.*, users.nom AS creator_name 
            FROM Events 
            LEFT JOIN users ON Events.creator_id = users.identifiant
        ''')
        events_info = cursor.fetchall()

        # Convertir chaque événement en dictionnaire
        col_names = [column[0] for column in cursor.description]
        events_info_dicts = [
            {col_names[index]: value for index, value in enumerate(event_info)}
            for
            event_info in events_info]

        return events_info_dicts
