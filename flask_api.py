from flask import Flask, request, jsonify, render_template
import psycopg2

app = Flask(__name__,template_folder='template')

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


@app.route("/search", methods=["GET"])
def search_data():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "No query provided. Please provide a query in address bar"})

    cur = conn.cursor()
    try:
        # Perform a partial text search in buyer_name, seller_name, or other_info columns
        cur.execute("SELECT * FROM Scrapped_Data WHERE buyer_name ILIKE %s OR seller_name ILIKE %s OR other_information ILIKE %s", ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
        data = cur.fetchall()
        cur.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})




@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
