from flask import Flask, render_template, request, redirect, session
import sqlite3
import requests 

app = Flask(__name__)
app.secret_key = "secret123"

API_KEY = "3ef9903e"

COUNTRIES = ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czechia", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea, North", "Korea, South", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"]
PHONE_CODES = ["+1 (US/Canada)", "+7 (Russia/Kazakhstan)", "+20 (Egypt)", "+27 (South Africa)", "+30 (Greece)", "+31 (Netherlands)", "+32 (Belgium)", "+33 (France)", "+34 (Spain)", "+36 (Hungary)", "+39 (Italy)", "+40 (Romania)", "+41 (Switzerland)", "+43 (Austria)", "+44 (UK)", "+45 (Denmark)", "+46 (Sweden)", "+47 (Norway)", "+48 (Poland)", "+49 (Germany)", "+51 (Peru)", "+52 (Mexico)", "+53 (Cuba)", "+54 (Argentina)", "+55 (Brazil)", "+56 (Chile)", "+57 (Colombia)", "+58 (Venezuela)", "+60 (Malaysia)", "+61 (Australia)", "+62 (Indonesia)", "+63 (Philippines)", "+64 (New Zealand)", "+65 (Singapore)", "+66 (Thailand)", "+81 (Japan)", "+82 (South Korea)", "+84 (Vietnam)", "+86 (China)", "+90 (Turkey)", "+91 (India)", "+92 (Pakistan)", "+93 (Afghanistan)", "+94 (Sri Lanka)", "+95 (Myanmar)", "+98 (Iran)", "+212 (Morocco)", "+213 (Algeria)", "+216 (Tunisia)", "+218 (Libya)", "+220 (Gambia)", "+221 (Senegal)", "+222 (Mauritania)", "+223 (Mali)", "+224 (Guinea)", "+225 (Ivory Coast)", "+226 (Burkina Faso)", "+227 (Niger)", "+228 (Togo)", "+229 (Benin)", "+230 (Mauritius)", "+231 (Liberia)", "+232 (Sierra Leone)", "+233 (Ghana)", "+234 (Nigeria)", "+235 (Chad)", "+236 (CAR)", "+237 (Cameroon)", "+244 (Angola)", "+254 (Kenya)", "+255 (Tanzania)", "+256 (Uganda)", "+351 (Portugal)", "+353 (Ireland)", "+355 (Albania)", "+358 (Finland)", "+359 (Bulgaria)", "+370 (Lithuania)", "+371 (Latvia)", "+372 (Estonia)", "+380 (Ukraine)", "+381 (Serbia)", "+385 (Croatia)", "+420 (Czechia)", "+421 (Slovakia)", "+503 (El Salvador)", "+504 (Honduras)", "+505 (Nicaragua)", "+506 (Costa Rica)", "+507 (Panama)", "+509 (Haiti)", "+591 (Bolivia)", "+593 (Ecuador)", "+595 (Paraguay)", "+598 (Uruguay)", "+880 (Bangladesh)", "+961 (Lebanon)", "+962 (Jordan)", "+963 (Syria)", "+964 (Iraq)", "+965 (Kuwait)", "+966 (Saudi Arabia)", "+968 (Oman)", "+971 (UAE)", "+972 (Israel)", "+973 (Bahrain)", "+974 (Qatar)", "+977 (Nepal)"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def get_db():
    return sqlite3.connect("database.db")


def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT)
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            movie TEXT,
            rating INTEGER,
            review TEXT)
    ''')

    conn.commit()
    conn.close()


init_db()


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            return redirect("/home")
        
        return render_template("login.html", error="invalid")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db()
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE email=?", (email,))
        existing_user = c.fetchone()

        if existing_user:
            conn.close()
            return render_template("register.html", error="exists", countries=COUNTRIES, phones=PHONE_CODES, months=MONTHS)

        c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("register.html", countries=COUNTRIES, phones=PHONE_CODES, months=MONTHS)


@app.route("/home", methods=["GET", "POST"])
def home():
    if "user_id" not in session:
        return redirect("/")

    movies = []

    if request.method == "POST":
        query = request.form["movie"]

        url = f"http://www.omdbapi.com/?s={query}&apikey={API_KEY}"
        response = requests.get(url).json()

        if "Search" in response:
            for item in response["Search"]:
                imdb_id = item["imdbID"]

                detail_url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={API_KEY}"
                details = requests.get(detail_url).json()

                movies.append(details)

    return render_template("home.html", movies=movies)


@app.route("/add_review", methods=["GET", "POST"])
def add_review():
    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":
        movie = request.form["movie"]
        rating = request.form["rating"]
        review = request.form["review"]

        conn = get_db()
        c = conn.cursor()
        c.execute(
            "INSERT INTO reviews (user_id, movie, rating, review) VALUES (?, ?, ?, ?)",
            (session["user_id"], movie, rating, review)
        )
        conn.commit()
        conn.close()

        return redirect("/home")

    movie_data = {
        "title": request.args.get("title"),
        "poster": request.args.get("poster"),
        "year": request.args.get("year"),
        "plot": request.args.get("plot"),
        "genre": request.args.get("genre"),
        "rating": request.args.get("imdb")
    }

    return render_template("add_review.html", movie=movie_data)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
    
if __name__ == "__main__":
    app.run(debug=True, port=5001)