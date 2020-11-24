from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import random



app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#Anadir campo de texto donde se pueda anadir la imagen del restaurante

class Restaurantes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    img_url = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(200), nullable=False) #Generar una tabla en el futuro
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    hor_abierto = db.Column(db.String(200), nullable=False)
    hor_cierre = db.Column(db.String(200), nullable=False)
    personas = db.Column(db.Integer, nullable=False)


#Añadir campo de texto donde se pueda anadir la imagen del producto


class Carrito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    id_pro = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    coste = db.Column(db.String(200), nullable=False)



class Productos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    id_res = db.Column(db.Integer, db.ForeignKey('restaurantes.id'), nullable=False)
    img_url = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)

class Usuarios(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean(), default = False, nullable = False )
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

#La ruta de acceso primaria principal
@app.route("/")
def home():
    productos = Productos.query.order_by(Productos.id).all()
    return render_template("home.html", productos = productos)


#El formulario de login completo, verificado
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == False:
        form = LoginForm()

        if form.validate_on_submit():
            user = Usuarios.query.filter_by(username=form.username.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user, remember=form.remember.data)
                    return redirect(url_for('home'))

            return render_template('login.html', form=form, error = "No esta registrado! \n Registrate!")    

        return render_template('login.html', form=form, error = "")
    else:
        return redirect(url_for('home'))  
   #  return render_template('login.html')


@app.route('/error')
def error():
    return render_template('error.html')


#Registro completado ya se puede decidir si ser admin o no 
@app.route("/register", methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated == False:
        form = RegisterForm()

        if form.validate_on_submit():
            try:
                hashed_password = generate_password_hash(form.password.data, method='sha256')
                admin = request.form['admin']
                if admin != 'No':
                    is_admin =  True
                    if admin == "res":
                        pass
                    else:
                        is_admin = False
                    new_user = Usuarios(username=form.username.data, email=form.email.data, password=hashed_password, is_admin = is_admin)
                    comp_user = Usuarios.query.filter_by(username=form.username.data).first()
                    comp_email = Usuarios.query.filter_by(email=form.email.data).first()
                
                    if comp_user is not None or comp_email is not None:
                        return render_template('register.html', form=form, error="El usuario o correo ya esta registrado! \n Ingrese uno diferente!")
                    else:
                        db.session.add(new_user)
                        db.session.commit()
                        return redirect(url_for('home'))
                else:
                    return render_template('register.html', form=form, error="No puede dejar la casilla de selección vacía!!")
            except:
                return redirect(url_for('error'))    
        return render_template('register.html', form=form , error="")
    else:
        return redirect(url_for('home')) 
    #return render_template("register.html")

#Ya se puede desloguear sin ningun problema 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

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
    productos = Productos.query.order_by(Productos.id).all()
    arr = []
    for pro in productos:
        query = db.engine.execute(f'SELECT img_url,tipo,nombre FROM Restaurantes WHERE id = {pro.id_res}')
        for row in query:
             #{% for arr in arr%}
             #{% if arr[0] ==  pro.id %}
             #    arr[1] y arr[2]
             #{% endif %}
            arr.append([row[0],row[1],row[2]])
    return render_template('productos.html', productos=productos, tipo=tipo, arr = arr)

@app.route("/restaurantes", methods=['GET', 'POST'])
def restaurants():
    tipo = "all"
    if request.method == 'POST':
        tipo = request.form.get("tipo")
    restaurantes = Restaurantes.query.order_by(Restaurantes.id).all()
    return render_template('restaurantes.html', restaurantes=restaurantes, tipo=tipo)

@app.route("/restaurantes/res/<int:id>", methods=['GET', 'POST'])
def rest_prods(id):
    restaurante = Restaurantes.query.get_or_404(id)
    productos = Productos.query.filter_by(id_res=restaurante.id).all()
    return render_template('restaurante.html', restaurante=restaurante, productos=productos)

@app.route("/restaurante", methods=['GET', 'POST'])
def restaurante():
    if request.method == 'POST':
        tipo = request.form['tipo'] # Esta al final sera una clave foranea a otra tabla 
        nombre = request.form['nombre']
        url = request.form['url']
        descripcion = request.form['descripcion']
        new_task = Restaurantes(id_user=current_user.id,tipo = tipo, nombre = nombre, img_url=url, descripcion = descripcion)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/restaurante')
        except:
            return 'No se pudo Agregar el restaurante'

    else:
        res = Restaurantes.query.order_by(Restaurantes.id).all()
        mis_res = Restaurantes.query.filter_by(id_user=current_user.id).all()
        return render_template('maestra_res.html', res=res, mis_res=mis_res)

#
#
#   Se viene bloque de codigo de todas las funcionalidades y rutas que tiene el admin
#   
#


@app.route('/consola/admin')
@login_required
def consola_admin():
    if current_user.is_admin:
        return render_template('admin/consola.html')
    else:
        return redirect(url_for('home'))


#Completada!
@app.route('/consola/admin/restaurantes', methods=['GET', 'POST'])
@login_required
def admin_res():
    if current_user.is_admin:
        restau = db.engine.execute(f'SELECT * FROM Restaurantes WHERE id_user = {current_user.id}')
        query = db.engine.execute(f'SELECT COUNT(*) FROM Restaurantes WHERE id_user = {current_user.id}')
        count = 0
        for q in query:
            count = q[0]
        restaurantes = []
        for res in restau:
            resta = [res[0],res[1],res[2],res[3],res[4],res[5],res[6],res[7],res[8]]
            restaurantes.append(resta)
        
        if request.method == 'POST':
            try:
                name = request.form['nombre']
                url_img = request.form['url_img']
                apertura = request.form['apertura']
                cierre = request.form['cierre']
                personas = int(request.form['personas'])
                descrip = request.form['descrip']
                tipo = request.form['Field5']
                res = Restaurantes(id_user = current_user.id, img_url = url_img, hor_abierto = apertura, hor_cierre = cierre,
                personas = personas, descripcion = descrip, tipo = tipo , nombre = name)
                try:
                    db.session.add(res)
                    db.session.commit()
                    return redirect(url_for('admin_res'))
                except:
                    return render_template('admin/restaurantes.html', rest = restaurantes, 
                    count = count, mensaje = "No se pudo agregar el restaurante!")

            except:
                return redirect(url_for('error'))
        else:
            return render_template('admin/restaurantes.html', rest = restaurantes, count = count)
    else:
        return redirect(url_for('home'))

#Completada
@app.route('/consola/admin/restaurantes/update/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_actualizar_res(id):
    if current_user.is_admin:
        user = db.engine.execute(f'SELECT COUNT(*) FROM Restaurantes WHERE id_user = {current_user.id} and id = {id}')
        for us in user:
            if us[0] == 0:
                return "Usted no tiene acceso a ese producto! Pillin"
        

        rest = Restaurantes.query.get_or_404(id)
        if  request.method == 'POST':
            rest.nombre = request.form['nombre']
            rest.img_url = request.form['url_img']
            rest.hor_abierto = request.form['apertura']
            rest.hor_cierre = request.form['cierre']
            rest.personas = int(request.form['personas'])
            rest.descripcion = request.form['descrip']
            rest.tipo = request.form['Field5']
            try:
                db.session.commit()
                return redirect(url_for('admin_res'))
            except:
                return redirect(url_for('error'))
        else:
            return render_template('/admin/actualizar_res.html',rest = rest)

    else:
        return redirect(url_for('home'))




#Completada!
@app.route('/consola/admin/restaurantes/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_borrar_res(id):
    if current_user.is_admin:
        user = db.engine.execute(f'SELECT COUNT(*) FROM Restaurantes WHERE id_user = {current_user.id} and {id}')
        for us in user:
            if us[0] == 0:
                return "Usted no tiene acceso a ese producto! Pillin"
        
        element_to_delete = Restaurantes.query.get_or_404(id)
        try:
            db.session.delete(element_to_delete)
            db.session.commit()
            return redirect(url_for('admin_res'))
        except:
            return redirect(url_for('error'))
            
    else:
        return redirect(url_for('home'))


@app.route('/consola/admin/productos', methods=['GET', 'POST'])
@login_required
def admin_pro():
    if current_user.is_admin:
        productos = db.engine.execute(f'SELECT * FROM Productos WHERE id_user = {current_user.id}')
        count_pro = 0
        prod = []
        for pro in productos:
            prod.append(pro)
            count_pro = count_pro + 1

        res = db.engine.execute(f'SELECT id,nombre FROM Restaurantes WHERE id_user = {current_user.id}')
        count_res = 0
        restaurantes = []
        for query in res:
            count_res = count_res + 1
            restaurantes.append(query)

        count = [count_pro,count_res]
        if request.method == 'POST':
            try:
                nombre = request.form['nombre']
                url_img = request.form['url_img']
                precio = request.form['precio']
                descrip = request.form['descrip']
                resta = request.form['admin']
                producto = Productos(id_user = current_user.id, id_res = resta ,img_url = url_img, 
                nombre = nombre, precio = precio, descripcion = descrip)

                try:
                    db.session.add(producto)
                    db.session.commit()
                    return redirect(url_for('admin_pro'))
                except:
                    return render_template('admin/productos.html',productos = prod, rest = restaurantes, 
                    count = count, mensaje = "No se pudo agregar el producto!")

            except:
                return redirect(url_for('error'))
        else:
            return render_template('admin/productos.html',productos = prod ,rest = restaurantes, count = count)
    else:
        return redirect(url_for('home'))



#Completada
@app.route('/consola/admin/productos/update/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_actualizar_pro(id):
    if current_user.is_admin:
        user = db.engine.execute(f'SELECT COUNT(*) FROM Productos WHERE id_user = {current_user.id} and id = {id}')
        for us in user:
            if us[0] == 0:
                return "Usted no tiene acceso a ese producto! Pillin"
        
        res = db.engine.execute(f'SELECT id,nombre FROM Restaurantes WHERE id_user = {current_user.id}')
        count_res = 0
        restaurantes = []
        for query in res:
            count_res = count_res + 1
            restaurantes.append(query)

        pro = Productos.query.get_or_404(id)
        if  request.method == 'POST':
            pro.nombre = request.form['nombre']
            pro.img_url = request.form['url_img']
            pro.precio = request.form['precio']
            pro.descripcion = request.form['descrip']
            pro.id_res = request.form['admin']

            try:
                db.session.commit()
                return redirect(url_for('admin_pro'))
            except:
                return redirect(url_for('error'))
        else:
            return render_template('/admin/actualizar_pro.html',pro = pro, rest = restaurantes)

    else:
        return redirect(url_for('home'))




#Completada!
@app.route('/consola/admin/productos/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_borrar_pro(id):
    if current_user.is_admin:
        user = db.engine.execute(f'SELECT COUNT(*) FROM Productos WHERE id_user = {current_user.id} and id = {id}')
        for us in user:
            if us[0] == 0:
                return "Usted no tiene acceso a ese producto! Pillin"
        
        element_to_delete = Productos.query.get_or_404(id)
        try:
            db.session.delete(element_to_delete)
            db.session.commit()
            return redirect(url_for('admin_pro'))
        except:
            return redirect(url_for('error'))
            
    else:
        return redirect(url_for('home'))



@app.route('/restaurante/producto/vista_compra/<int:id>', methods=['GET', 'POST'])
def vista_producto(id):
    pro = Productos.query.get_or_404(id)
    query = db.engine.execute(f'SELECT tipo,hor_abierto,hor_cierre FROM Restaurantes WHERE id = {pro.id_res}')
    now = datetime.now()
    hora_actual = str(now.time())[0:5]
    abierto = ""
    cierre = ""

    for q in query:
        tipo = q[0]
        abierto = q[1]
        cierre = q[2]

    horas = [abierto,cierre]
    ac_ho, ac_min = hora_actual.split(":")
    ab_ho , ab_min = abierto.split(':')
    cie_ho , cie_min = cierre.split(':')
    if int(ac_ho) >= int(ab_ho) and int(ac_ho) <= int(cie_ho):
        #if int(ac_min) >= int(ab_min):
        if request.method == 'POST':
            if not current_user.is_admin:
                gaseosa = int(request.form['Field5'])
                cantidad = int(request.form['cantidad'])
                cart = Carrito(id_user = current_user.id, id_pro = id, cantidad = cantidad, coste = str((int(pro.precio) + gaseosa)))
                try:
                    db.session.add(cart)
                    db.session.commit()
                    return redirect(url_for('carrito'))
                except:
                    return redirect(url_for('error'))
            else:
                return render_template("/carrito/vista_producto.html" , producto = pro, tipo = tipo, mess = "Eres un admin! No puedes tener un carrito",horas = horas)         

        else:
            return render_template("/carrito/vista_producto.html" , producto = pro, tipo = tipo, mess = "",horas = horas)    
    else:
        return render_template("/carrito/vista_producto.html" , producto = pro, tipo = tipo, mess = "El restaurante esta cerrado de momento",horas = horas)    
    


@app.route('/restaurante/producto/carrito', methods=['GET', 'POST'])
def carrito():
    if not current_user.is_admin:
        return render_template('carrito/carrito.html')
    else:
        return redirect(url_for('home'))


if __name__ == "__main__":
    hashed_password = generate_password_hash("12345678", method='sha256')
    new_user = Usuarios(username="admin", email="admon.sojas@gmail.com",
                    is_admin=True, password=hashed_password)
    comp_user = Usuarios.query.filter_by(username="admin").first()
    comp_email = Usuarios.query.filter_by(email="admon.sojas@gmail.com").first()
    if comp_user is not None or comp_email is not None:
        pass
    else:
        db.session.add(new_user)
        db.session.commit()
    app.run(debug=True)     
