from flask import Flask, request, jsonify, render_template
import psycopg2

app = Flask(__name__,template_folder='templates')

# Connect to PostgreSQL
conn = psycopg2.connect(
database="Web Scrapper",
    user="postgres",
    password="Abhi1234@5",
    host="localhost",
    port="5433",
)


@app.route("/api/by_doc_no/")
def show():
    return ("Please enter document number on to address bar")

@app.route("/api/by_year/")
def show2():
    return ("Please enter year on to address bar")

# Fetch data by Document No.
@app.route("/api/by_doc_no/<doc_no>")
def get_data_by_doc_no(doc_no):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Scrapped_Data WHERE registration_number = %s", (doc_no,))
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

# Fetch data by Year of Registration
@app.route("/api/by_year/<year>")
def get_data_by_year(year):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Scrapped_Data WHERE EXTRACT(YEAR from Year) = %s", (year,))
    data = cur.fetchall()
    cur.close()
    return jsonify(data)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
