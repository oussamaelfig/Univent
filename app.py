import sqlite3
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)


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

        # Connect to SQLite
        con = sqlite3.connect("db/database.db")
        cur = con.cursor()

        # Insert event into the database
        cur.execute(
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
        con.commit()
        con.close()

        return "Event created successfully"

    return render_template("create_event.html")


if __name__ == "__main__":
    app.run()
