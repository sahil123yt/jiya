from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_medicines():
    with open('medicines.json') as f:
        return json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shop')
def shop():
    medicines = load_medicines()
    return render_template('shop.html', medicines=medicines)

@app.route('/add_to_cart/<string:medicine_id>')
def add_to_cart(medicine_id):
    medicines = load_medicines()
    medicine = next((m for m in medicines if m['id'] == medicine_id), None)

    if 'cart' not in session:
        session['cart'] = []

    if medicine:
        session['cart'].append(medicine)
        session.modified = True

    return redirect(url_for('shop'))

@app.route('/cart')
def cart():
    return render_template('cart.html', cart=session.get('cart', []))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        new_medicine = {
            "id": request.form['id'],
            "name": request.form['name'],
            "price": request.form['price']
        }
        medicines = load_medicines()
        medicines.append(new_medicine)
        with open('medicines.json', 'w') as f:
            json.dump(medicines, f, indent=2)
        return redirect('/admin')
    medicines = load_medicines()
    return render_template('admin.html', medicines=medicines)

if __name__ == '__main__':
    app.run(debug=True)