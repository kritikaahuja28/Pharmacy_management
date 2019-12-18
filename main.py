from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, SelectField

app = Flask(__name__)
app.config['MEDICINE_DATABASE'] = 'sqlite:///medicine.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class medicine(db.Model):
   id = db.Column('num',db.Integer(),primary_key='TRUE')
   name = db.Column( db.String(100))
   quantity = db.Column(db.Integer())
   price = db.Column(db.Integer())
   shelf = db.Column(db.Integer()) 
   expiry = db.Column(db.Integer())

   def __init__(self, name,quantity, price, shelf,expiry):
      self.name = name
      self.quantity = quantity
      self.price = price
      self.shelf = shelf
      self.expiry = expiry

class bill(db.Model):
   id = db.Column('num',db.Integer(),primary_key='TRUE')
   bill_name = db.Column( db.String(100))
   bill_total = db.Column(db.Integer())
   bill_mode = db.Column(db.String(10))
   bill_quantity = db.Column(db.Integer()) 

   def __init__(self, id,bill_name,bill_quantity, bill_total, bill_mode):
      self.id = id
      self.bill_name = bill_name
      self.bill_quantity = bill_quantity
      self.bill_total = bill_total
      self.bill_mode = bill_mode
      
class medicineSearchForm(Form):
    choices = [('name', 'name'),
               ('quantity', 'quantity'),
               ('price', 'price'),('shelf', 'shelf'),('expiry', 'expiry')]
    select = SelectField('Search for medicine:', choices=choices)
    search = StringField('')



@app.route('/data')
def data():
   return render_template('data.html', medicine = medicine.query.all() )

@app.route('/option')
def option():
   return render_template('option.html')

@app.route('/bill_data')
def bill_data():
   return render_template('bill.html', bill = bill.query.all() )

@app.route('/bill_form', methods = ['GET', 'POST'])
def bill_form():
   if request.method == 'POST':
      if not request.form.get('id') or not request.form.get('bill_name') or not request.form.get('bill_quantity') or not request.form.get('bill_total') or not request.form.get('bill_mode'):
         flash('Please enter all the fields', 'error')
      else:
         BILL = bill(request.form['id'],request.form['bill_name'],request.form['bill_quantity'], request.form['bill_total'], request.form['bill_mode'])
         db.session.add(BILL)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('bill_data'))
   return render_template('bill_form.html')

@app.route('/form', methods = ['GET', 'POST'])
def form():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['quantity'] or not request.form['price'] or not request.form['expiry'] or not request.form['shelf']:
         flash('Please enter all the fields', 'error')
      else:
         MEDICINES = medicine(request.form['name'],request.form['quantity'], request.form['price'], request.form['shelf'], request.form['expiry'])
         db.session.add(MEDICINES)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('data'))
   return render_template('forms.html')
@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
      if request.form.get('username',False) == 'medicine' and request.form.get('password',False) == 'admin':
        return redirect(url_for('option'))
            
      else:error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/index', methods=['GET', 'POST'])
def index():
    search = medicineSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html', form=search)
@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']
    if search.data['search'] == '':
        qry = db_session.query(medicine)
        results = qry.all()
    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        return render_template('data.html', results=results)

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)