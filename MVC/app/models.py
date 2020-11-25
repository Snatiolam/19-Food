
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

from app import db

'''

Creacion de todas las clases correspondientes al manejo de
la base de datos. (Modelo)
'''

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
    password = db.Column(db.String(200), nullable=False) 

class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    id_res = db.Column(db.Integer, db.ForeignKey('restaurantes.id'), nullable=False)
    id_pro = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.String(200), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    tiempo = db.Column(db.String(200), nullable=False)
    entregado = db.Column(db.Boolean(), default = False, nullable = False )

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    id_res = db.Column(db.Integer, db.ForeignKey('restaurantes.id'), nullable=False)
    hora = db.Column(db.String(200), nullable=False)
    num_personas = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.String(200), nullable=False)


#Creacion cuenta admin 
hashed_password = generate_password_hash("12345678", method='sha256')
new_user = Usuarios(username="admin", email="admin@gmail.com",
                        is_admin=True, password=hashed_password)
comp_user = Usuarios.query.filter_by(username="admin").first()
comp_email = Usuarios.query.filter_by(email="admin@gmail.com").first()
if comp_user is not None or comp_email is not None:
    pass
else:
    db.session.add(new_user)
    db.session.commit()
                
#Creacion cuenta santiago
hashed_password = generate_password_hash("12345678", method='sha256')
new_user = Usuarios(username="salzatec1", email="salzatec1@gmail.com",
                        is_admin=True, password=hashed_password)
comp_user = Usuarios.query.filter_by(username="salzatec1").first()
comp_email = Usuarios.query.filter_by(email="salzatec1@gmail.com").first()
if comp_user is not None or comp_email is not None:
    pass
else:
    db.session.add(new_user)
    db.session.commit()

#Creacion cuenta sebastian
hashed_password = generate_password_hash("12345678", method='sha256')
new_user = Usuarios(username="surregog", email="surregog@gmail.com",
                        is_admin=True, password=hashed_password)
comp_user = Usuarios.query.filter_by(username="surregog").first()
comp_email = Usuarios.query.filter_by(email="surregog@gmail.com").first()
if comp_user is not None or comp_email is not None:
    pass
else:
    db.session.add(new_user)
    db.session.commit()
    
# Usuarios Normales
hashed_password = generate_password_hash("12345678", method='sha256')
new_user = Usuarios(username="normal1", email="normal1@gmail.com",
                        is_admin=False, password=hashed_password)
comp_user = Usuarios.query.filter_by(username="normal1").first()
comp_email = Usuarios.query.filter_by(email="normal1@gmail.com").first()
if comp_user is not None or comp_email is not None:
    pass
else:
    db.session.add(new_user)
    db.session.commit()

hashed_password = generate_password_hash("12345678", method='sha256')
new_user = Usuarios(username="normal2", email="normal2@gmail.com",
                        is_admin=False, password=hashed_password)
comp_user = Usuarios.query.filter_by(username="normal2").first()
comp_email = Usuarios.query.filter_by(email="normal2@gmail.com").first()
if comp_user is not None or comp_email is not None:
    pass
else:
    db.session.add(new_user)
    db.session.commit()

hashed_password = generate_password_hash("12345678", method='sha256')
new_user = Usuarios(username="normal3", email="normal3@gmail.com",
                        is_admin=False, password=hashed_password)
comp_user = Usuarios.query.filter_by(username="normal3").first()
comp_email = Usuarios.query.filter_by(email="normal3@gmail.com").first()
if comp_user is not None or comp_email is not None:
    pass
else:
    db.session.add(new_user)
    db.session.commit()

#Creacion cuenta admin 
user = Usuarios.query.filter_by(username="admin").first()
new_restaurant = Restaurantes(id_user=user.id, img_url="https://10619-2.s.cdn12.com/rests/original/327_356523056.jpg", tipo="RAP",nombre="Mandingas",hor_abierto="05:00",hor_cierre="22:00",personas=12) 
comp_rest = Restaurantes.query.filter_by(nombre="Mandingas").first()
if comp_rest is not None:
    pass
else:
    db.session.add(new_restaurant)
    db.session.commit()

new_restaurant = Restaurantes(id_user=user.id, img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTvdG_k7keQLh0vrkrjPI6h99uQAqJOfoScsQ&usqp=CAU", tipo="PER",nombre="Sabor Peru",hor_abierto="05:00",hor_cierre="22:00",personas=12) 
comp_rest = Restaurantes.query.filter_by(nombre="Sabor Peru").first()
if comp_rest is not None:
    pass
else:
    db.session.add(new_restaurant)
    db.session.commit()

new_restaurant = Restaurantes(id_user=user.id, img_url="https://img.freepik.com/vector-gratis/logos-restaurantes-mexicanos-contorno_23-2147546379.jpg?size=338&ext=jpg", tipo="MEX",nombre="Mister Taco",hor_abierto="05:00",hor_cierre="22:00",personas=12) 
comp_rest = Restaurantes.query.filter_by(nombre="Mister Taco").first()
if comp_rest is not None:
    pass
else:
    db.session.add(new_restaurant)
    db.session.commit()

'''
Usuario salzatec1
'''

user = Usuarios.query.filter_by(username="salzatec1").first()

new_restaurant = Restaurantes(id_user=user.id, img_url="https://pbs.twimg.com/media/D26_z5ZX4AEGGli.jpg", tipo="COL",nombre="Mondongo's",hor_abierto="05:00",hor_cierre="22:00",personas=12) 
comp_rest = Restaurantes.query.filter_by(nombre="Mondongo's").first()
if comp_rest is not None:
    pass
else:
    db.session.add(new_restaurant)
    db.session.commit()

new_restaurant = Restaurantes(id_user=user.id, img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSVoxUWnlaqnEwo4gwXzHxTodSeOeosGTgfQA&usqp=CAU", tipo="ALT",nombre="Liguria artesanal",hor_abierto="05:00",hor_cierre="22:00",personas=12) 
comp_rest = Restaurantes.query.filter_by(nombre="Liguria artesanal").first()
if comp_rest is not None:
    pass
else:
    db.session.add(new_restaurant)
    db.session.commit()

new_restaurant = Restaurantes(id_user=user.id, img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQgXux0VzOt5zIpJGMuyaaDbtCYMUpD-KZeQ&usqp=CAU", tipo="ITA",nombre="Ragazzi",hor_abierto="05:00",hor_cierre="22:00",personas=12) 
comp_rest = Restaurantes.query.filter_by(nombre="Ragazzi").first()
if comp_rest is not None:
    pass
else:
    db.session.add(new_restaurant)
    db.session.commit()

'''
Usuario surregog
'''

user = Usuarios.query.filter_by(username="surregog").first()

new_restaurant = Restaurantes(id_user=user.id, img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRkapkVzPf_MGxrA2LSgjwu_6hh71nm42ZbIw&usqp=CAU", tipo="MEX",nombre="El chacho",hor_abierto="05:00",hor_cierre="22:00",personas=12) 
comp_rest = Restaurantes.query.filter_by(nombre="El chacho").first()
if comp_rest is not None:
    pass
else:
    db.session.add(new_restaurant)
    db.session.commit()

new_restaurant = Restaurantes(id_user=user.id, img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHFtW8DxZdO2lyRLarotEQA9e9BckptlSpHg&usqp=CAU", tipo="PER",nombre="Miraflores",hor_abierto="05:00",hor_cierre="22:00",personas=12) 
comp_rest = Restaurantes.query.filter_by(nombre="Miraflores").first()
if comp_rest is not None:
    pass
else:
    db.session.add(new_restaurant)
    db.session.commit()

new_restaurant = Restaurantes(id_user=user.id, img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzBvQZv2QFuNasiNMHI3Z20Th9g2SNR4xmCg&usqp=CAU", tipo="RAP",nombre="Los perritos",hor_abierto="05:00",hor_cierre="22:00",personas=12) 
comp_rest = Restaurantes.query.filter_by(nombre="Los perritos").first()
if comp_rest is not None:
    pass
else:
    db.session.add(new_restaurant)
    db.session.commit()

##############
restaurante = Restaurantes.query.filter_by(nombre="Mandingas").first()

nombre_prod = "Papas de mil"
new_prod = Productos(id_user=restaurante.id_user,id_res=restaurante.id, img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRmumd11_PNklyA_cRLPTMgGia2qn8_2nEbPw&usqp=CAU", nombre=nombre_prod, precio=24, descripcion="")
comp_prod = Productos.query.filter_by(nombre=nombre_prod).first()
if comp_prod is not None:
    pass
else:
    db.session.add(new_prod)
    db.session.commit()

nombre_prod = "Papas de tres mil"
new_prod = Productos(id_user=restaurante.id_user,id_res=restaurante.id, img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQCmxILS9ripctXnqVhdKEegEyQY8sioNwEng&usqp=CAU", nombre=nombre_prod, precio=24, descripcion="")
comp_prod = Productos.query.filter_by(nombre=nombre_prod).first()
if comp_prod is not None:
    pass
else:
    db.session.add(new_prod)
    db.session.commit()
##########
restaurante = Restaurantes.query.filter_by(nombre="Sabor Peru").first()

nombre_prod = "Mariscos ricos"
new_prod = Productos(id_user=restaurante.id_user,id_res=restaurante.id, img_url="https://dam.cocinafacil.com.mx/wp-content/uploads/2014/03/Parrillada-de-mariscos.jpg", nombre=nombre_prod, precio=24, descripcion="")
comp_prod = Productos.query.filter_by(nombre=nombre_prod).first()

if comp_prod is not None:
    pass
else:
    db.session.add(new_prod)
    db.session.commit()

nombre_prod = "Langosta"
new_prod = Productos(id_user=restaurante.id_user,id_res=restaurante.id, img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ0VoR0DBLMBLuRnB9vWIXR1tNeMS6WXPwn9A&usqp=CAU", nombre=nombre_prod, precio=24, descripcion="")
comp_prod = Productos.query.filter_by(nombre=nombre_prod).first()
if comp_prod is not None:
    pass
else:
    db.session.add(new_prod)
    db.session.commit()
##########
restaurante = Restaurantes.query.filter_by(nombre="Ragazzi").first()

nombre_prod = "Pasta con leche"
new_prod = Productos(id_user=restaurante.id_user,id_res=restaurante.id, img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREsVOZBueQZ31anT_z2nV6FSy10gP44qEtGA&usqp=CAU", nombre=nombre_prod, precio=24, descripcion="")
comp_prod = Productos.query.filter_by(nombre=nombre_prod).first()

if comp_prod is not None:
    pass
else:
    db.session.add(new_prod)
    db.session.commit()

nombre_prod = "Macarrones con queso"
new_prod = Productos(id_user=restaurante.id_user,id_res=restaurante.id, img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSR7uRTlaj0gRQV-RuRyFv3Y6Cl5WtpWA_bfg&usqp=CAU", nombre=nombre_prod, precio=24, descripcion="")
comp_prod = Productos.query.filter_by(nombre=nombre_prod).first()
if comp_prod is not None:
    pass
else:
    db.session.add(new_prod)
    db.session.commit()
##########
restaurante = Restaurantes.query.filter_by(nombre="Los perritos").first()

nombre_prod = "Perro"
new_prod = Productos(id_user=restaurante.id_user,id_res=restaurante.id, img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTwBGsdZfANJ4Yr1-JPXi9DZ0L9Njrfr513bA&usqp=CAU", nombre=nombre_prod, precio=24, descripcion="")
comp_prod = Productos.query.filter_by(nombre=nombre_prod).first()

if comp_prod is not None:
    pass
else:
    db.session.add(new_prod)
    db.session.commit()

nombre_prod = "Hamburguesa"
new_prod = Productos(id_user=restaurante.id_user,id_res=restaurante.id, img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT6hKm8spfh1t7GIQnvZLH_s2Zn--3ChQpKUg&usqp=CAU", nombre=nombre_prod, precio=24, descripcion="")
comp_prod = Productos.query.filter_by(nombre=nombre_prod).first()
if comp_prod is not None:
    pass
else:
    db.session.add(new_prod)
    db.session.commit()
