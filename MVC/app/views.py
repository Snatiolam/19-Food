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


from app.models import *

from app import login_manager, app, bootstrap 

@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(int(user_id))

'''

Clases que se encargan de gestionar operaciones con autenticacion y registro

'''

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

'''

Creacion de todas las rutas con sus respectivos
funciones (Controladores)

'''

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


# Ruta de error
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

#Ya se puede desloguear sin ningun problema 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/products", methods=['GET', 'POST'])
def product():
    tipo = "all"
    productos = Productos.query.order_by(Productos.id).all()
    arr = []
    for pro in productos:
        query = db.engine.execute(f'SELECT img_url,tipo,nombre FROM Restaurantes WHERE id = {pro.id_res}')
        for row in query:
            #           img_url, tipo, nombre
            arr.append([row[0], row[1], row[2]])
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

'''

Se viene bloque de codigo de todas las funcionalidades y rutas que tiene el admin

'''

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
@login_required
def carrito():
    if not current_user.is_admin:
        productos_cart = db.engine.execute(f'SELECT * FROM Carrito WHERE id_user = {current_user.id}')
        count = 0
        total = 0
        productos = []
        for pro in productos_cart:
            query = db.engine.execute(f'SELECT * FROM Productos WHERE id = {pro.id_pro}')
            for row in query:
                # Id del carrito, nommbre producto, cantidad, precio, imagen
                total = total + (int(pro[4]) * int(pro[3]))
                productos.append([pro[0], row[4], pro[3], pro[4], row[3]])
            count = count + 1
            total = total + 5 
        return render_template('carrito/carrito.html',productos = productos, count = count, total = total)
    else:
        return redirect(url_for('home'))

@app.route('/restaurante/producto/carrito/del/<int:id>', methods=['GET', 'POST'])
@login_required
def del_carrito(id):
    if not current_user.is_admin:
        persona = db.engine.execute(f'SELECT COUNT(*) FROM Carrito WHERE id_user = {current_user.id} and id = {id}')
        for row in persona:
            if row[0] < 1:
                return "No puedes realizar esta acción pillín"
        

        element_to_delete = Carrito.query.get_or_404(id)
        try:
            db.session.delete(element_to_delete)
            db.session.commit()
            return redirect(url_for('carrito'))
        except:
            return redirect(url_for('error'))

    else:
        return redirect(url_for('home'))

@app.route('/restaurante/producto/carrito/tarjeta', methods=['GET', 'POST'])
@login_required
def tarjeta():
    if not current_user.is_admin:
        rand = random.randint(15,55)
        if request.method == 'POST':
            productos_cart = db.engine.execute(f'SELECT * FROM Carrito WHERE id_user = {current_user.id}')
            for pro in productos_cart:
                query = db.engine.execute(f'SELECT * FROM Productos WHERE id = {pro.id_pro}')
                for row in query:
                    now = datetime.now()
                    hora_actual = str(now.time())[0:5]
                    try:
                        registro = Registro(id_user = current_user.id,id_res = row[2], id_pro = row[0], precio = row[5], cantidad = pro[3],
                        tiempo = hora_actual, entregado = False)
                        db.session.add(registro)
                    except:
                        return redirect(url_for('error'))
            

            cart_del = db.engine.execute(f'DELETE FROM Carrito WHERE id_user = {current_user.id}')
            db.session.commit()
            return redirect(url_for('consola_usuario'))
        else:
            return render_template('/carrito/tarjeta.html', rand = rand)
    else:
        return redirect(url_for('home'))


@app.route('/restaurante/producto/carrito/efectivo', methods=['GET', 'POST'])
@login_required
def efectivo():
    if not current_user.is_admin:
        rand = random.randint(15,55)
        if request.method == 'POST':
            productos_cart = db.engine.execute(f'SELECT * FROM Carrito WHERE id_user = {current_user.id}')
            for pro in productos_cart:
                query = db.engine.execute(f'SELECT * FROM Productos WHERE id = {pro.id_pro}')
                for row in query:
                    now = datetime.now()
                    hora_actual = str(now.time())[0:5]
                    try:
                        registro = Registro(id_user = current_user.id,id_res = row[2] ,id_pro = row[0], precio = row[5], cantidad = pro[3],
                        tiempo = hora_actual)
                        db.session.add(registro)
                    except:
                        return redirect(url_for('error'))


            cart_del = db.engine.execute(f'DELETE FROM Carrito WHERE id_user = {current_user.id}')
            db.session.commit()
            return redirect(url_for('consola_usuario'))
        else:
            return render_template('/carrito/efectivo.html', rand = rand)
    else:
        return redirect(url_for('home'))


@app.route('/consola/usuario', methods=['GET', 'POST'])
@login_required
def consola_usuario():
    if not current_user.is_admin:
        return render_template('/consola_user.html')
    else:
        return redirect(url_for('home'))


@app.route('/quienes_somos', methods=['GET', 'POST'])
def somos():
    return render_template('somos.html')


@app.route('/consola/admin/pedidos')
@login_required
def admin_pedidos():
    if current_user.is_admin:
        query = db.engine.execute(f'SELECT id FROM Restaurantes WHERE id_user = {current_user.id}')
        productos = []
        count = 0
        for row in query:
            pendiente = db.engine.execute(f'SELECT * FROM Registro WHERE id_res = {row[0]}')
            for product in pendiente:
                productos.append(product)
                count = count + 1

        return render_template('admin/pedidos.html', count = count, productos = productos)
    else:
        return redirect(url_for('home'))


@app.route('/consola/admin/pedidos/update/estado/<int:id>')
@login_required
def actualizar_pedidos(id):
    if current_user.is_admin:
        query = db.engine.execute(f'SELECT id FROM Restaurantes WHERE id_user = {current_user.id}')
        productos = []
        count = 0
        tiene = False
        for row in query:
            pendiente = db.engine.execute(f'SELECT COUNT(*) FROM Registro WHERE id_res = {row[0]}')
            for product in pendiente:
                if product[0] != 0:
                    tiene = True
                
        if not tiene:
            return "No puedes estar aqui"
        else:
            productos = Registro.query.get_or_404(id)
            productos.entregado = True
            try:
                db.session.commit()
                return redirect(url_for('admin_pedidos'))
            except:
                return redirect(url_for('error'))
    else:
        return redirect(url_for('home'))


@app.route('/consola/admin/pedidos/restrasar/estado/<int:id>')
@login_required
def retrasar_pedidos(id):
    if current_user.is_admin:
        query = db.engine.execute(f'SELECT id FROM Restaurantes WHERE id_user = {current_user.id}')
        productos = []
        count = 0
        tiene = False
        for row in query:
            pendiente = db.engine.execute(f'SELECT COUNT(*) FROM Registro WHERE id_res = {row[0]}')
            for product in pendiente:
                if product[0] != 0:
                    tiene = True
                
        if not tiene:
            return "No puedes estar aqui"
        else:
            productos = Registro.query.get_or_404(id)
            now = datetime.now()
            hora_actual = str(now.time())[0:5]
            productos.tiempo = hora_actual
            try:
                db.session.commit()
                return redirect(url_for('admin_pedidos'))
            except:
                return redirect(url_for('error'))
    else:
        return redirect(url_for('home'))


@app.route('/reserva/<int:id>' , methods=['GET', 'POST'])
@login_required
def reserva(id):
    if not current_user.is_admin:
        restaurante = Restaurantes.query.get_or_404(id)
        query = db.engine.execute(f'SELECT tipo,hor_abierto,hor_cierre FROM Restaurantes WHERE id = {id}')
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
        mensaje = ""
        horas = [abierto,cierre]
        date = now.date()
        if int(ac_ho) >= int(ab_ho) and int(ac_ho) <= int(cie_ho):
            if request.method == 'POST':
                personas = request.form['cantidad']
                fecha = request.form['fecha']
                hora,minuto = str(request.form['hora']).split(':')
                tiempo = request.form['hora']
                
                try:
                    query = db.engine.execute(f'SELECT COUNT(*) FROM Reserva WHERE id_user = {current_user.id} and fecha = {fecha}')
                    for row in query:
                        if row[0] != 0 :
                            return render_template("reserva.html", pro = restaurante, mensaje = "No puedes hacer mas de una reserva por día",date = date , horas = horas)
                    
                    reserva = Reserva(id_user = current_user.id, id_res = id, hora = tiempo, num_personas = personas,
                    fecha = fecha)
                    db.session.add(reserva)
                    db.session.commit()
                    return redirect(url_for('consola_usuario'))
                except:
                    return redirect('error')
            else:
                return render_template("reserva.html", pro = restaurante, mensaje = mensaje,date = date , horas = horas)
        else:
            return render_template("reserva.html", pro = restaurante, mensaje = "El restaurante esta cerrado de momento",date = date, horas = horas)
    else:
        return redirect(url_for('login'))

