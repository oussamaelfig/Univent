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

    def get_users(self):
        cursor = self.get_connexion().cursor()
        cursor.execute("select * from users")
        return cursor.fetchall()

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

    def get_courriel_from_id_session(self, id_session):
        cursor = self.get_connexion().cursor()
        cursor.execute(
            "select courriel from users inner join sessions on users.identifiant = userId where sessions.identifiant=?",
            (id_session,))
        return cursor.fetchone()[0]

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
    
    def get_events(self):
        cursor = self.get_connexion().cursor()
        cursor.execute("select * from Events")
        return cursor.fetchall()

    def get_all_events(self, creator_id):
        connect = self.get_connexion()
        cursor = connect.cursor()
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

        # Convert each event into a dictionary
        col_names = [column[0] for column in cursor.description]
        events_info_dicts = [
            {col_names[index]: value for index, value in enumerate(event_info)}
            for event_info in events_info
        ]

        return events_info_dicts

    def register_participant(self, event_id, nom, email):
        connect = self.get_connexion()
        cursor = connect.cursor()

        cursor.execute(
            "INSERT INTO Participants (event_id, nom, email) VALUES (?, ?, ?)",
            (event_id, nom, email),
        )

        connect.commit()

        return cursor.lastrowid

    def get_all_particiapnt_by_courriel(self, courriel):
        cursor = self.get_connexion().cursor()
        cursor.execute(
            "select Events.event_id, title, location, start_date_time, end_date_time, description from Events inner join Participants on Participants.event_id=Events.event_id where email=?",
            (courriel,))
        return cursor.fetchall()

    def search_events(self, title_q=None, description_q=None, organizer_q=None,
                      start=None, end=None, max_participants=None):
        conn = self.get_connexion()
        cursor = conn.cursor()

        query = """
            SELECT Events.*, users.nom AS creator_name
            FROM Events
            LEFT JOIN users ON Events.creator_id = users.identifiant
            WHERE 1
            """

        params = []

        if title_q:
            query += " AND LOWER(Events.title) LIKE LOWER(?)"
            params.append('%' + title_q + '%')

        if description_q:
            query += " AND LOWER(Events.description) LIKE LOWER(?)"
            params.append('%' + description_q + '%')

        if organizer_q:
            query += " AND LOWER(users.nom) LIKE LOWER(?)"
            params.append('%' + organizer_q + '%')

        if start:
            query += " AND DATE(Events.start_date_time) >= DATE(?)"
            params.append(start.split('T')[0])

        if end:
            query += " AND DATE(Events.end_date_time) <= DATE(?)"
            params.append(end.split('T')[0])

        if max_participants:
            query += " AND Events.max_registration <= ?"
            params.append(max_participants)

        cursor.execute(query, params)

        col_names = [column[0] for column in cursor.description]
        events_info_dicts = [
            {col_names[index]: value for index, value in enumerate(event_info)}
            for event_info in cursor.fetchall()
        ]

        return events_info_dicts
