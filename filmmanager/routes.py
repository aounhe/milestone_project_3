from flask import render_template, request, redirect, url_for, flash
from filmmanager import app, db
from filmmanager.models import Film, Review, Users
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/films", methods=["GET", "POST"])
def films():
    films = list(Film.query.order_by(Film.id_film, Film.title, Film.director, Film.year,
                                     Film.genre, Film.image, Film.overview).all())
    return render_template("films.html", films=films)




@app.route("/signup", methods=["GET", "POST"])
def signup():
    """ Register section for the user to create their own user account, if the user request to Post,
    then the user would need to fill the form and click submit"""
    if request.method == "POST":
        id_email = request.form.get("id_email")
        password = request.form.get("password")
        fname = request.form.get("fname")
        lname = request.form.get("lname")

        # Hash the password before storing it
        # Hash the password before storing it to the database so the password is save.
        password_hash = generate_password_hash(password)

        # Check if the user with the given email already exists
        # Check if the user with the given email already exists,
        #  if it exists it will print a message
        existing_user = Users.query.filter_by(id_email=id_email).first()

        if existing_user:
            flash('Email already in use. Please choose a different email.', 'error')
            return redirect(url_for("signup"))
        # Create a new Users instance with hashed password
        user = Users(
            id_email=id_email,
            password=password_hash,
            fname=fname,
            lname=lname
        )
        # Add the user to the database
        db.session.add(user)
        db.session.commit()

        # Once the account it is create it will get redirected to this site.
        return redirect(url_for("profile"))

    return render_template("signup.html")


@app.route("/signin", methods=["GET"])
def signin():
    """
    if request.method == "GET":
        users = Users(
            id_email = request.form.get("id_email"),
            password = request.form.get("password"),
        )
        db.session.add(users)
        db.session.commit()
        return redirect(url_for("profile"))
    """
    return render_template("signin.html")


@app.route("/profile", methods=["GET", "POST"])
def profile():

    return render_template("profile.html")


@app.route("/add_review", methods=["GET", "POST"])
def add_review():
    """When the user clicks 'Add Review' button in the profile page, this will use the'GET'
       method and render the 'add_review' template. Once they submit the form, this
       will call the same function, but will check if the request being made is a “POST“ method,
       which posts data somewhere, such as a database. """
    if request.method == "POST":
        # add a review to the database.
        # if I use request method I have to import it to flask as well on the top.
        review = Review(
            film_id=request.form.get("film_id"),
            review_text=request.form.get("review_text"),
            users_review=request.form.get("users_review")
        )
        db.session.add(review)
        db.session.commit()
        # after the form gets submitted, and I have added and committed
        # the new data to our database, I can redirect the user to the 'profile' page.
        return redirect(url_for("films"))
    return render_template("add_review.html")
