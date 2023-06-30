import sqlite3
from flask import Flask, render_template, request, g, session, redirect
from werkzeug.utils import secure_filename
from database import Database
import uuid
import hashlib
import re

app = Flask(__name__)


def get_db():
    if getattr(g, "_database", None) is None:
        g._database = Database()
    return g._database


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


@app.route("/contact")
def contact():  # put application's code here
    return render_template("contact.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/create_event", methods=["GET", "POST"])
def create_event():
    if request.method == "POST":
        title = request.form["title"]
        start_date_time = request.form["start_date_time"]
        end_date_time = request.form["end_date_time"]
        location = request.form["location"]
        description = request.form["description"]

        flyer_image_name = None

        flyer_image = request.files["flyer_image"]
        if flyer_image:
            flyer_image_name = secure_filename(flyer_image.filename)
            flyer_image.save("db/flyerImages/" + flyer_image_name)

        # TODO: Trouver une facon pour Get le creator_id
        #  mettre en place un mécanisme pour obtenir l'identifiant de
        #  l'utilisateur actuellement connecté qui est en train de créer
        #  l'événement. Cela pourrait être fait en utilisant un système
        #  d'authentification et de session.
        creator_id = 1
        # utilise la class Database pour faire le traitement.
        get_db().creer_new_evenement(creator_id, title, start_date_time,
                                     end_date_time,
                                     location, flyer_image_name, description)

        return "Event created successfully"

    return render_template("create_event.html")


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
        while(get_db().get_user_from_iden(identifiant) is not None):
            identifiant = uuid.uuid4().hex
        salt = uuid.uuid4().hex
        hache = hashlib.sha512(str(mdp + salt).encode("utf-8")).hexdigest()
        get_db().creer_user(identifiant, nom, courriel, type_compte, hache, salt)
        return redirect('/succes_compte')
    return render_template("create_account.html")

@app.route("/login", methods=["POST", "GET"])
def connecter():
    if request.method == "POST":
       if "id" not in session:
           courriel = request.form["courriel"]
           mdp = request.form["mdp"]
           err = ["Le courriel et/ou le nom d'usager sont erronés"]
           if courriel == "" or mdp == "":
               return render_template("login.html", erreurs=err)
           
       else:
           return redirect("/user_page") # TODO. check le hub
    else:
        return render_template("login.html") 
        

def valider_compte(nom, courriel):
    err = []
    regex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    if nom == "" or len(nom) > 100:
        err.append("Le nom entré est invalide (100 caractères maximum).")
    if courriel == "" or len(courriel) > 100 or not re.fullmatch(regex, courriel): #REGEX EST COURRIEL.
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


if __name__ == "__main__":
    app.run()

app.secret_key = "qweiqen1@!@#SADASFA@#!!!+_$"
