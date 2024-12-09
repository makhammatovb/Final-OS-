from flask import Flask, render_template, request
import pg8000

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        level = request.form["level"]
        return render_template("timetable.html", level=level, data=[], message="Loading timetable...")

    return render_template("index.html")


@app.route("/timetable", methods=["GET"])
def timetable():
    level = request.args.get('level')
    if not level:
        return "Level not provided", 400

    conn = pg8000.connect(
        user="postgres",
        password="postgres",
        host="postgres.ctscw2waepuq.eu-north-1.rds.amazonaws.com",
        port=5432,
        database="postgres"
    )

    cur = conn.cursor()
    query = "SELECT * FROM Timetable WHERE level = %s;"
    cur.execute(query, (level,))
    rows = cur.fetchall()
    if rows:
        return render_template("timetable.html", level=level, data=rows, message="")
    else:
        return render_template("timetable.html", level=level, data=[], message="No data found for this level.")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
