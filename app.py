from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#Anadir campo de texto donde se pueda anadir la imagen del restaurante

class Restaurantes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(200), nullable=False) #Generar una tabla en el futuro
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)

#Anadir campo de texto donde se pueda anadir la imagen del producto

class Productos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False) # Hash, pero por ahora inseguro y directo
    email = db.Column(db.String(200), nullable=False)

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
        content = request.form['content']
        price = request.form['price']
        new_task = Productos(nombre = name, precio = price, descripcion = content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/productos')
        except:
            return 'No se pudo poner el producto'

    else:
        productos = Productos.query.order_by(Productos.id).all()
        return render_template('maestra_pro.html', productos=productos)

@app.route("/restaurante", methods=['GET', 'POST'])
def restaurante():
    if request.method == 'POST':
        tipo = request.form['tipo'] # Esta al final sera una clave foranea a otra tabla 
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        new_task = Restaurantes(tipo = tipo, nombre = nombre, descripcion = descripcion)

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
    app.run(debug=True)     
