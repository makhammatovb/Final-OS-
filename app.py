from flask import Flask, render_template, request
import pg8000

app = Flask(__name__)

DB_CONFIG = {
    "user": "postgres",
    "password": "postgres",
    "host": "postgres.ctscw2waepuq.eu-north-1.rds.amazonaws.com",
    "port": 5432,
    "database": "postgres"
}

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/timetable", methods=["GET"])
def timetable():
    level = request.args.get('level')
    if not level:
        return render_template("timetable.html", level=None, data=[], message="No level selected.")

    levels_map = {
        "1": "Undergraduate",
        "2": "Graduate"
    }

    level_label = levels_map.get(level)
    if not level_label:
        return render_template("timetable.html", level=None, data=[], message="Invalid level selected.")

    try:
        conn = pg8000.connect(**DB_CONFIG)
        cur = conn.cursor()
        query = "SELECT * FROM Timetable WHERE level = %s;"
        cur.execute(query, (level_label,))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        if rows:
            return render_template("timetable.html", level=level_label, data=rows, message="")
        else:
            return render_template("timetable.html", level=level_label, data=[], message="No data found for this level.")
    except Exception as e:
        return render_template("timetable.html", level=None, data=[], message=f"Error: {e}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
