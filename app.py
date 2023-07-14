import base64
import hashlib
import re
import sqlite3
import uuid
from functools import wraps

from database import Database
from flask import (Flask, Response, flash, g, redirect, render_template,
                   request, session, url_for)
from werkzeug.utils import secure_filename

app = Flask(__name__)


def get_db():
    if getattr(g, "_database", None) is None:
        g._database = Database()
    return g._database


def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated(session):
            return send_unauthorized()
        return f(*args, **kwargs)

    return decorated


def organisation_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_organisation(session):
            return send_unauthorized()
        return f(*args, **kwargs)

    return decorated

def etudiant_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_etudiant(session):
            return send_unauthorized()
        return f(*args, **kwargs)


def is_etudiant(sessionId):
    return get_db().get_type_compte_from_session_id(session["id"])[0] == 1

def is_organisation(sessionId):
    return get_db().get_type_compte_from_session_id(session["id"])[0] == 0


# Ne regarde pas le type d'utilisateur. Seulement qu'il soit authentifié
def is_authenticated(session):
    if ("id" in session and
            get_db().get_session_id_from_id_session(session["id"]) is
            not None):
        return True
    return False


def send_unauthorized():
    return render_template("erreur.html", err="401"), 401


@app.errorhandler(404)
def retourner404(err):
    return render_template("erreur.html", err="404"), 404


@app.errorhandler(400)
def retourner400(err):
    return render_template("erreur.html", err="400"), 400


@app.errorhandler(500)
def retourner500(err):
    return render_template("erreur.html", err="500"), 500


@app.teardown_appcontext
def close_db(exeption):
    if getattr(g, "_database", None) is not None:
        g._database.close_connection()


@app.route("/")
def hello_world():  # put application's code here
    return render_template("index.html")


@app.route("/faq")
def faq():  # put application's code here
    return render_template("faq.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/events')
def events():
    events = get_db().get_all_events_by_all_users()
    # Convertir l'image BLOB en une chaîne base64 pour chaque événement
    for event in events:
        if event['flyer_image']:
            event['flyer_image'] = base64.b64encode(
                event['flyer_image']).decode('utf-8')

    print(events)
    return render_template('events.html', events=events)


@app.route("/create_event", methods=["GET", "POST"])
@authentication_required
@organisation_required
def create_event():
    if request.method == "POST":
        title = request.form["title"]
        start_date_time = request.form["start_date_time"]
        end_date_time = request.form["end_date_time"]
        location = request.form["location"]
        description = request.form["description"]
        max_registration = request.form["max_registration"]

        # Basic validation
        if not title:
            flash("Veuillez entrer un Titre à votre événement", "error")
            return render_template("create_event.html")
        if not start_date_time or not end_date_time:
            flash("Les heures de début et de fin sont requises", "error")
            return render_template("create_event.html")
        if not location:
            flash("L'emplacement est requis", "error")
            return render_template("create_event.html")
        if not description:
            flash("La description est obligatoire", "error")
            return render_template("create_event.html")
        if not max_registration or int(max_registration) < 1:
            flash("L'inscription maximale est requise et doit être d'au "
                  "moins 5 personnes",
                  "error")
            return render_template("create_event.html")

        flyer_image_blob = None

        flyer_image = request.files["flyer_image"]
        if flyer_image:
            flyer_image_blob = flyer_image.read()

        creator_id = get_db().get_id_user_from_id_session(session['id'])[0]
        # utilise la class Database pour faire le traitement.
        event_id = get_db().creer_new_evenement(
            creator_id,
            title,
            start_date_time,
            end_date_time,
            location,
            flyer_image_blob,
            description,
            max_registration
        )

        # Flash message
        flash("Votre évenement a été créé !", "success")

        # Redirect to the new event's page
        return redirect(url_for('event_info', event_id=event_id))

    return render_template("create_event.html")


@app.route('/event_info/<int:event_id>')
@authentication_required
def event_info(event_id):
    # Get the event's information from the database
    event_info = get_db().get_event_info(event_id)

    # Convert the BLOB image to a base64 string
    if event_info['flyer_image']:
        event_info['flyer_image'] = base64.b64encode(
            event_info['flyer_image']).decode('utf-8')

    # Render a template with the event's information
    return render_template('event_info.html', event=event_info)


@app.route("/user_page/<identifiant>", methods=["GET", "POST"])
@authentication_required
def user_page(identifiant):
    user_info = get_db().get_user_info_from_iden(identifiant)
    events = get_db().get_all_events(identifiant)
    return render_template("user_page.html", events=events,
                           user_info=user_info)


@app.route("/modify_event/<int:event_id>", methods=["POST"])
@authentication_required
@organisation_required
def modify_event(event_id):
    if request.method == "POST":
        title = request.form.get("title")
        start_date_time = request.form.get("start_date_time")
        end_date_time = request.form.get("end_date_time")
        location = request.form.get("location")
        description = request.form.get("description")
        max_registration = request.form.get("max_registration")

        flyer_image_blob = None

        flyer_image = request.files.get("flyer_image")
        if flyer_image:
            flyer_image_blob = flyer_image.read()

        # utilise la class Database pour faire le traitement.
        get_db().modify_event(
            event_id,
            title,
            start_date_time,
            end_date_time,
            location,
            flyer_image_blob,
            description,
            max_registration,
        )
        flash(f"Modification de l'événement '{title}' effectuée !", "success")
        return redirect("/user_page/" + get_db().get_id_user_from_id_session(
            session["id"])[0])


@app.route("/delete_event/<int:event_id>", methods=["POST"])
@authentication_required
@organisation_required
def delete_event(event_id):
    event = get_db().get_event_by_id(event_id)
    get_db().delete_event(event_id)

    flash(f"Événement '{event[2]}' supprimé !", "success")
    return redirect("/user_page/" + get_db().get_id_user_from_id_session(
        session["id"])[0])


@app.route("/succes_compte")
def afficher_succes():
    return render_template("succes_compte.html")


@app.route("/create_account", methods=["GET", "POST"])
def creer_compte():
    if request.method == "POST":
        nom = request.form["nom"]
        courriel = request.form["courriel"]
        mdp = request.form["mdp"]
        mdp_conf = request.form["mdpConf"]
        type_compte = request.form["type"]
        err = []
        if get_db().get_user_from_courriel(courriel) is not None:
            err.append("Un compte existe déjà avec ce courriel.")
            return render_template("create_account.html", erreurs=err)
        err = valider_compte(nom, courriel)
        err2 = valider_mdp(mdp, mdp_conf)
        for e in err2:
            err.append(e)
        if len(err) != 0:
            return render_template("create_account.html", erreurs=err)
        identifiant = uuid.uuid4().hex
        while (get_db().get_user_from_iden(identifiant) is not None):
            identifiant = uuid.uuid4().hex
        salt = uuid.uuid4().hex
        hache = hashlib.sha512(str(mdp + salt).encode("utf-8")).hexdigest()
        get_db().creer_user(identifiant, nom, courriel, type_compte, hache,
                            salt)
        return redirect('/succes_compte')
    if "id" in session:
        return redirect("/user_page/" + get_db().get_id_user_from_id_session(
            session["id"])[0])
    return render_template("create_account.html")


@app.route("/login", methods=["POST", "GET"])
def connecter():
    if request.method == "POST":
        if "id" not in session:
            courriel = request.form["courriel"]
            mdp = request.form["mdp"]
            err = ["Le courriel et/ou le nom d'usager sont erronés"]
            if courriel == "" or mdp == "" or len(courriel) > 100:
                return render_template("login.html", erreurs=err)
            utilisateur = get_db().get_user_pass_from_courriel(courriel)
            if utilisateur is None:
                return render_template("login.html", erreurs=err)
            salt = utilisateur[1]
            mdp_entre = hashlib.sha512(
                str(mdp + salt).encode("utf-8")).hexdigest()
            if mdp_entre == utilisateur[0]:
                id_session = uuid.uuid4().hex
                get_db().creer_session(id_session, utilisateur[2])
                session["id"] = id_session
                return redirect("/user_page/" + utilisateur[2])
            else:
                return render_template("login.html", erreurs=err)
        else:
            return redirect(
                "/user_page/" + get_db().get_id_user_from_id_session(
                    session["id"])[0])
    else:
        if "id" not in session:
            return render_template("login.html")
        return redirect("/user_page/" + get_db().get_id_user_from_id_session(
            session["id"])[0])


@authentication_required
@app.route("/logout")
def deconnecter():
    get_db().delete_session(session["id"])
    session["id"] = None;
    session.pop("id", None)
    return redirect('/')


def valider_compte(nom, courriel):
    err = []
    regex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    if nom == "" or len(nom) > 100:
        err.append("Le nom entré est invalide (100 caractères maximum).")
    if courriel == "" or len(courriel) > 100 or not re.fullmatch(regex,
                                                                 courriel):  # REGEX EST COURRIEL.
        err.append("Le courriel entré est invalide.")
    return err


def valider_mdp(mdp, mdp2):
    err = []
    a_err = False
    punctuation = ['!', ',', '?', '.', '¡', ';', '¿']
    if mdp == "" or len(mdp) < 8:
        err.append("Le mot de passe entré est invalide.")
        a_err = True
    if re.search('[0-9]', mdp) is None and not a_err:
        err.append("Le mot de passe entré est invalide.")
        a_err = True
    if re.search('[A-Z]', mdp) is None and not a_err:
        err.append("Le mot de passe entré est invalide.")
        a_err = True
    for c in mdp:
        if c in punctuation and not a_err:
            return err
    if not a_err:
        err.append("Le mot de passe entré est invalide.")
    if mdp != mdp2:
        err.append("Les deux mots de passe ne concordent pas.")
    return err

@etudiant_required
@app.route("/register/<int:event_id>", methods=["POST"])
def register(event_id):
    nom = request.form.get("nom")
    email = request.form.get("email")

    get_db().register_participant(event_id, nom, email)

    # retourne une réponse HTTP 200 si l'inscription est réussie
    return "", 200


if __name__ == "__main__":
    app.run()

app.secret_key = "qweiqen1@!@#SADASFA@#!!!+_$"
