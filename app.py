import sqlite3
from flask import Flask, render_template, request, g, session
from werkzeug.utils import secure_filename
from database import Database
import re

app = Flask(__name__)

def get_db():
    if getattr(g, "_database", None) is None:
        g._database = Database()
    return g._database

@app.teardown_appcontext
def fermer_app():
    if getattr(g, "_database", None) is None:
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

        # Handle the image upload
        flyer_image = request.files["flyer_image"]
        if flyer_image:
            flyer_image_name = secure_filename(flyer_image.filename)
            flyer_image.save("db/flyerImages" + flyer_image_name)

        # TODO: Trouver une facon pour Get le creator_id
        #  mettre en place un mécanisme pour obtenir l'identifiant de
        #  l'utilisateur actuellement connecté qui est en train de créer
        #  l'événement. Cela pourrait être fait en utilisant un système
        #  d'authentification et de session.
        creator_id = 1
        # utilise la class Database pour faire le traitement.
        get_db().creer_new_evenement(creator_id, title, start_date_time, end_date_time,
                                     location, flyer_image_name, description)
        
        return "Event created successfully"

    return render_template("create_event.html")


@app.route("/create_account", methods=["GET", "POST"])
def creer_compte():
    if request.method == "POST":
        nom = request.form["nom"]
        courriel = request.form["courriel"]
        mdp = request.form["mdp"]
        mdp_conf = request.form["mdpConf"]
        type_compte = request["type"]
        err = valider_compte(nom, courriel, type_compte)
        err.insert(valider_mdp(mdp, mdp_conf))
        if len(err) != 0:
            return render_template("create_account.html", erreurs=err) 
        # creer dans bd.
    return render_template("create_account.html")
    

def valider_compte(nom, courriel, type_compte):
    err = []
    regex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    if nom == "" or len(nom) < 100:
        err.insert("Le nom entré est invalide (100 caractères maximum).")
    if courriel == "" or len(courriel) < 100 or not re.fullmatch(regex, courriel): #REGEX EST COURRIEL.
        err.insert("Le courriel entré est invalide.")
    return err

def valider_mdp(mdp, mdp2):
    err = []
    a_err = False
    punctuation = ['!', ',', '?', '.', '¡', ';', '¿']
    if mdp == "" or len(mdp):
        err.insert("Le mot de passe entré est invalide.")
        a_err = True
    if re.search('[0-9]', mdp) is None and not a_err:
        err.insert("Le mot de passe entré est invalide.")
        a_err = True
    if re.search('[A-Z]', mdp) is None and not a_err:
        err.insert("Le mot de passe entré est invalide.")
        a_err = True
    for c in mdp:
        if c in punctuation and not a_err:
            return err
    err.insert("Le mot de passe entré est invalide.")    
    if mdp != mdp2:
        err.insert("Les deux mots de passe ne concordent pas.")
    return err

if __name__ == "__main__":
    app.run()

app.secret_key = "qweiqen1@!@#SADASFA@#!!!+_$"