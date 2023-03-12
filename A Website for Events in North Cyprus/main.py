from flask import *
from dbscript import *

app = Flask(__name__)

app.secret_key = "super secret key"


# Home page
@app.route("/")
def index():
    if 'username' in session:
        events = get_city_events()
        cities = get_citynames()
        return render_template("index.html", username=session['username'], events=events, cities=cities)
    else:
        return render_template("index.html")


# Register
@app.route("/register")
def register():
    error = request.args.get("error", 0)
    if error == 0:
        return render_template("register.html", error="")
    return render_template("register.html", error=error)


# Register error
@app.route("/registererror", methods=["POST"])
def registererror():
    error = request.form["error"]
    return redirect(url_for("register", error=error))


# Login
@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = escape(request.form["username"])
        password = escape(request.form["password"])
        check = False

        for user in get_users():
            if user[0] == username and user[3] == password:
                check = True

        if check:
            session["username"] = username
            return redirect(url_for('index'))
        else:
            return render_template("user404.html")

    elif request.method == "GET":
        pass


# Logout
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


# Add user
@app.route("/adduser", methods=["POST"])
def adduser():
    username = request.form["username"]
    password = request.form["password"]
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    email = request.form["email"]

    # check if username already exist in database
    names = get_usernames()

    if username not in names:
        insert_user(username, firstname, lastname, password, email)
        return render_template("registerconfirmation.html", username=username)
    else:
        return redirect(url_for("register", error="Username already exist in database"))


# List existing user
@app.route("/listexistinguser")
def list_existing_user():
    names = get_usernames()
    suggestions = []
    q = request.args.get("q", None)
    if q != None:
        for name in names:
            if q.lower() == name[0:len(q)].lower():
                suggestions.append(name)
    return ", ".join(suggestions)


# Render event form
@app.route("/renderEventForm")
def event_form():
    return render_template("createevent.html", city_list=get_citynames())


# Display events
@app.route("/displayEvents")
def display_events():
    events = get_events_by_username(session["username"])
    cities = get_citynames()
    return render_template("displayevents.html", events=events, cities=cities)


# Add event
@app.route("/addevent", methods=["POST"])
def add_event():
    name = request.form["name"]
    description = request.form["description"]
    location = request.form["location"]
    price = request.form["ticket_price"]
    date = request.form["date"]
    time = request.form["time"]
    cityid = get_cityid_by_cityname(request.form["city"])

    insert_event(name, description, price, date, time,
                 location, cityid, session["username"])
    return render_template("addeventconfirmation.html", event_name=name)


# Deactivate event
@app.route("/deactivateEvent/<eventid>")
def _deactivate_event(eventid):
    deactivate_event(eventid)
    return redirect(url_for("display_events"))


# Show event details
@app.route("/eventDetails/<eventid>")
def event_details(eventid):
    event = get_event_by_eventid(eventid)
    cityname = get_cityname_by_cityid(event[0][8])
    return render_template("eventdetails.html", event=event[0], cityname=cityname)


@app.route("/keywordSearch")
def keyword_search():
    keyword = request.args.get("keyword", None)
    events = get_events_by_keyword(keyword)
    return render_template("keywordsearch.html", events=events)


if __name__ == "__main__":
    app.run()
