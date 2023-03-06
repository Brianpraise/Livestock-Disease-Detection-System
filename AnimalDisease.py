import sqlite3
from flask import Flask, request, render_template
import pickle
import pandas as pd

app = Flask(__name__)
d = pd.read_csv(r'E:\Brianpraise\Brianpraise\Animal-Disease-Prediction\Animal_Disease_dataset.csv')
model = pickle.load(open(r"E:\Brianpraise\Brianpraise\Animal-Disease-Prediction\random.pkl", "rb"))

# create database connection and cursor objects
conn = sqlite3.connect('Animal.db')
c = conn.cursor()

# create table to store livestock data
c.execute('''CREATE TABLE IF NOT EXISTS animal 
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              AnimalName VARCHAR(255),
              symptoms1 VARCHAR(255),
              symptoms2 VARCHAR(255),
              symptoms3 VARCHAR(255),
              symptoms4 VARCHAR(255),
              symptoms5 VARCHAR(255),
              Disease VARCHAR(255))''')


# close cursor and connection objects

@app.route("/")
def home():
    AnimalName=sorted(d['AnimalName'].unique())
    symptoms1=sorted(d['symptoms1'].unique())
    symptoms2=sorted(d['symptoms2'].unique())
    symptoms3=sorted(d['symptoms3'].unique())
    symptoms4=sorted(d['symptoms4'].unique())
    symptoms5=sorted(d['symptoms5'].unique())
    AnimalName.insert(0, 'Select AnimalName')
    symptoms1.insert(0, 'Select symptom1')
    symptoms2.insert(0, 'Select symptom2')
    symptoms3.insert(0, 'Select symptom3')
    symptoms4.insert(0, 'Select symptom4')
    symptoms5.insert(0, 'Select symptom5')
    return render_template("Home.html",AnimalName=AnimalName,symptoms1=symptoms1,symptoms2=symptoms2,symptoms3=symptoms3,symptoms4=symptoms4,symptoms5=symptoms5)

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        # Columns Reading
        AnimalName = request.form.get("AnimalName")
        symptoms1 = request.form.get("symptoms1")
        symptoms2 = request.form.get("symptoms2")
        symptoms3 = request.form.get("symptoms3")
        symptoms4 = request.form.get("symptoms4")
        symptoms5 = request.form.get("symptoms5")
        
        prediction = model.predict(pd.DataFrame([[AnimalName, symptoms1, symptoms2, symptoms3, symptoms4, symptoms5]],columns=['AnimalName', 'symptoms1', 'symptoms2', 'symptoms3','symptoms4', 'symptoms5']))
        prediction_text = "Animal Disease is. {}".format(prediction)
        # insert data into the database
        conn = sqlite3.connect('Animal.db')
        c = conn.cursor()
        print(f"AnimalName: {AnimalName}")  # print the value of the AnimalName variable
        c.execute('INSERT INTO animal (AnimalName, symptoms1, symptoms2, symptoms3, symptoms4, symptoms5, Disease) VALUES (?, ?, ?, ?, ?, ?, ?)', (AnimalName, symptoms1, symptoms2, symptoms3, symptoms4, symptoms5, prediction_text))
        conn.commit()
        c.close()
        conn.close()
        return render_template('Home.html', prediction_text=prediction_text)

    return render_template("Home.html")
@app.route("/report", methods=["GET", "POST"])
def generate_report():
    if request.method == "POST":
        conn = sqlite3.connect('Animal.db')
        c = conn.cursor()
        c.execute("SELECT * FROM animal")
        rows = c.fetchall()
        c.close()
        conn.close()
        return render_template("report.html", rows=rows)
    return render_template("Home.html")


if __name__ == "__main__":
    app.run(debug=True)
