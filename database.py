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
        cursor.execute("insert into users(identifiant, nom, typeCompte, courriel, hache, salt)"
                       "values(?,?,?,?,?,?)", 
                       (identifiant, nom, type_c, courriel, hache, salt,))
        connection.commit()
            
    def get_user_from_iden(self, ident):
        cursor = self.get_connexion().cursor()
        cursor.execute("select identifiant from users where identifiant = ?", (ident, ))
        return cursor.fetchone()
    
    def get_user_from_courriel(self, courriel):
        cursor = self.get_connexion().cursor()
        cursor.execute("select identifiant from users where courriel = ?", (courriel, ))
        return cursor.fetchone()
    
    def get_user_pass_from_courriel(self, courriel):
        cursor = self.get_connexion().cursor()
        cursor.execute("select hache, salt, identifiant from users where courriel = ?", (courriel, ))
        return cursor.fetchone()
    
    #### Table sessions ####
    def creer_session(self, sessionId, userId):
        connection = self.get_connexion()
        cursor = connection.cursor()
        cursor.execute("insert into sessions values(identifiant, userId)")
        
    def get_id_user_from_id_session(self, id_session):
        cursor = self.get_connexion().cursor()
        cursor.execute("select userId from sessions where identifiant=?", (id_session, ))
        return cursor.fetchone()
    
    #### Table events #####
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
