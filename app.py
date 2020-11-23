from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#Anadir campo de texto donde se pueda anadir la imagen del restaurante

class Restaurantes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(200), nullable=False) #Generar una tabla en el futuro
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)

#Anadir campo de texto donde se pueda anadir la imagen del producto

class Productos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)

class Usuarios(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False, nullable=False)
    password = db.Column(db.String(200), nullable=False) # Hash, pero por ahora inseguro y directo

@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def registro():
    return render_template("register.html")

@app.route("/productos", methods=['GET', 'POST'])
def productos():
    if request.method == 'POST':
        
        name = request.form['nombre']
        url = request.form['url']
        content = request.form['content']
        price = request.form['price']
        new_task = Productos(nombre = name,img_url=url, precio = price, descripcion = content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/productos')
        except:
            return 'No se pudo poner el producto'

    else:
        productos = Productos.query.order_by(Productos.id).all()
        return render_template('maestra_pro.html', productos=productos)

@app.route("/products", methods=['GET', 'POST'])
def product():
    tipo = "all"
    if request.method == 'POST':
        tipo = request.form.get("tipo")
    productos = Productos.query.order_by(Productos.id).all()
    return render_template('productos.html', productos=productos, tipo=tipo)


@app.route("/restaurante", methods=['GET', 'POST'])
def restaurante():
    if request.method == 'POST':
        tipo = request.form['tipo'] # Esta al final sera una clave foranea a otra tabla 
        nombre = request.form['nombre']
        url = request.form['url']
        descripcion = request.form['descripcion']
        new_task = Restaurantes(tipo = tipo, nombre = nombre, img_url=url, descripcion = descripcion)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/restaurante')
        except:
            return 'No se pudo Agregar el restaurante'

    else:
        res = Restaurantes.query.order_by(Restaurantes.id).all()
        return render_template('maestra_res.html', res=res)

@app.route('/delete/<int:id>')
def delete_producto(id):
    product_to_delete = Productos.query.get_or_404(id)

    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect('/productos')
    except:
        return 'Tuvimos problemas eliminando el producto, intentelo de nuevo'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_producto(id):
    productos = Productos.query.get_or_404(id)

    if request.method == 'POST':
        productos.nombre = request.form['nombre']
        productos.descripcion = request.form['content']
        productos.precio = request.form['price']
        try:
            db.session.commit()
            return redirect('/productos')
        except:
            return 'Hubo problemas actualizando el producto'

    else:
        return render_template('update_pro.html', productos=productos)

@app.route('/delete/res/<int:id>')
def delete_res(id):
    res_to_delete = Restaurantes.query.get_or_404(id)

    try:
        db.session.delete(res_to_delete)
        db.session.commit()
        return redirect('/restaurante')
    except:
        return 'Tuvimos problemas eliminando el restaurante, intentelo de nuevo'

@app.route('/update/res/<int:id>', methods=['GET', 'POST'])
def update_res(id):
    res = Restaurantes.query.get_or_404(id)

    if request.method == 'POST':
        res.nombre = request.form['nombre']
        res.descripcion = request.form['descripcion']
        res.tipo = request.form['tipo']
        try:
            db.session.commit()
            return redirect('/restaurante')
        except:
            return 'Hubo problemas actualizando el Restaurante'

    else:
        return render_template('update_res.html', res=res)

if __name__ == "__main__":
    hashed_password = generate_password_hash("12345678", method="sha256")
    new_user = Usuarios(username="admin", email="admin@gmail.com", is_admin=True,password=hashed_password)
    comp_user = Usuarios.query.filter_by(username="admin").first()
    comp_email = Usuarios.query.filter_by(email="admin@gmail.com")
    if comp_user is not None or comp_email is not None:
        pass
    else:
        db.session.add(new_user)
        db.session.commit()
    app.run(debug=True)     
