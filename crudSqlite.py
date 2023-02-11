from flask import Flask, request, jsonify, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    brand = db.Column(db.String(80), nullable=False)
    year = db.Column(db.String(80), nullable=False)
    daily = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String(80), nullable=False)
    observation = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def dict(self):
       return {"id":self.id, 
               "name":self.name, 
               "email":self.email, 
               "model":self.model, 
               "brand":self.brand, 
               "year":self.year, 
               "daily":self.daily, 
               "image":self.image, 
               "observation":self.observation,
               "status":self.status}

with app.app_context():
    db.create_all()

@app.route('/index.html', methods=['GET'])
def initial():
    return render_template('index.html')


@app.route('/veiculos.html', methods=['GET'])
def vehicles():
    return render_template('veiculos.html', car = Cars.query.all())


@app.route('/edit.html', methods=['GET'])
def editvehicles():
    return render_template('edit.html', car = Cars.query.all())


@app.route('/add', methods=['POST'])
def add_car():
    car = Cars(name = request.form['name'], 
                email = request.form['email'], 
                model = request.form['model'], 
                brand = request.form['brand'], 
                year = request.form['year'], 
                daily = request.form['daily'], 
                image = request.form['image'], 
                observation = request.form['observation'], 
                status = "new")
    db.session.add(car)
    db.session.commit()
    return render_template('veiculos.html', car = Cars.query.all())


# PUT request to update a contact
@app.route('/car/<int:id>', methods=['PUT', 'POST'])
def update_car(id):
    car = db.get_or_404(Cars, id)
    car.model = request.form['model']
    car.brand = request.form['brand']
    car.year = request.form['year']
    car.daily = request.form['daily']
    car.observation = request.form['observation']
    car.status = request.form['status']
    db.session.commit()
    return render_template('edit.html', car = Cars.query.all())

@app.route("/delete/<int:id>", methods=["POST"])
def car_delete(id):
    car = db.get_or_404(Cars, id)
    db.session.delete(car)
    db.session.commit()
    return render_template('edit.html', car = Cars.query.all())

if __name__ == '__main__':
    app.run(debug=True,port=5001)
