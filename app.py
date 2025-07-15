from flask import Flask, request, render_template_string

app = Flask(__name__)

kunden = {
    "B-AB123": {"termin": None},
    "M-XY987": {"termin": None}
}

termine = [
    "2025-07-22 10:00",
    "2025-07-23 11:00",
    "2025-07-24 09:00"
]

@app.route('/')
def home():
    return open("index.html").read()

@app.route('/login', methods=['POST'])
def login():
    plate = request.form['plate'].strip().upper()
    if plate in kunden:
        freie_termine = [t for t in termine if t not in [k['termin'] for k in kunden.values()]]
        return render_template_string(open("templates/termine.html").read(), plate=plate, termine=freie_termine)
    return "Kennzeichen nicht gefunden", 404

@app.route('/book', methods=['POST'])
def book():
    plate = request.form['plate']
    termin = request.form['termin']
    if plate in kunden and termin:
        kunden[plate]['termin'] = termin
        return f"<h2>Termin am {termin} für {plate} erfolgreich gebucht.</h2>"
    return "Fehler bei der Buchung", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
