from app import *

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

nombre_prod = "Maricos ricos"
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
