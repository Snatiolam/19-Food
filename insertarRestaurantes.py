from app import *

#Creacion cuenta admin 
user = Usuarios.query.filter_by(username="admin").first()
new_restaurant = Restaurantes(id_user=user.id, img_url="https://10619-2.s.cdn12.com/rests/original/327_356523056.jpg", tipo="RAP",nombre="Mandingas",hor_abierto="09:00",hor_cierre="10:00",personas=12) 
comp_rest = Restaurantes.query.filter_by(nombre="Mandingas").first()
if comp_rest is not None:
    pass
else:
    db.session.add(new_restaurant)
    db.session.commit()

new_restaurant = Restaurantes(id_user=user.id, img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTvdG_k7keQLh0vrkrjPI6h99uQAqJOfoScsQ&usqp=CAU", tipo="PER",nombre="Sabor Peru",hor_abierto="09:00",hor_cierre="10:00",personas=12) 
comp_rest = Restaurantes.query.filter_by(nombre="Sabor Peru").first()
if comp_rest is not None:
    pass
else:
    db.session.add(new_restaurant)
    db.session.commit()

new_restaurant = Restaurantes(id_user=user.id, img_url="https://img.freepik.com/vector-gratis/logos-restaurantes-mexicanos-contorno_23-2147546379.jpg?size=338&ext=jpg", tipo="MEX",nombre="Mister Taco",hor_abierto="09:00",hor_cierre="10:00",personas=12) 
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

new_restaurant = Restaurantes(id_user=user.id, img_url="https://pbs.twimg.com/media/D26_z5ZX4AEGGli.jpg", tipo="COL",nombre="Mondongo's",hor_abierto="09:00",hor_cierre="10:00",personas=12) 
comp_rest = Restaurantes.query.filter_by(nombre="Mondongo's").first()
if comp_rest is not None:
    pass
else:
    db.session.add(new_restaurant)
    db.session.commit()

new_restaurant = Restaurantes(id_user=user.id, img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSVoxUWnlaqnEwo4gwXzHxTodSeOeosGTgfQA&usqp=CAU", tipo="ALT",nombre="Liguria artesanal",hor_abierto="09:00",hor_cierre="10:00",personas=12) 
comp_rest = Restaurantes.query.filter_by(nombre="Liguria artesanal").first()
if comp_rest is not None:
    pass
else:
    db.session.add(new_restaurant)
    db.session.commit()

new_restaurant = Restaurantes(id_user=user.id, img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQgXux0VzOt5zIpJGMuyaaDbtCYMUpD-KZeQ&usqp=CAU", tipo="ITA",nombre="Ragazzi",hor_abierto="09:00",hor_cierre="10:00",personas=12) 
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

new_restaurant = Restaurantes(id_user=user.id, img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRkapkVzPf_MGxrA2LSgjwu_6hh71nm42ZbIw&usqp=CAU", tipo="MEX",nombre="El chacho",hor_abierto="09:00",hor_cierre="10:00",personas=12) 
comp_rest = Restaurantes.query.filter_by(nombre="El chacho").first()
if comp_rest is not None:
    pass
else:
    db.session.add(new_restaurant)
    db.session.commit()

new_restaurant = Restaurantes(id_user=user.id, img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTHFtW8DxZdO2lyRLarotEQA9e9BckptlSpHg&usqp=CAU", tipo="PER",nombre="Miraflores",hor_abierto="09:00",hor_cierre="10:00",personas=12) 
comp_rest = Restaurantes.query.filter_by(nombre="Miraflores").first()
if comp_rest is not None:
    pass
else:
    db.session.add(new_restaurant)
    db.session.commit()

new_restaurant = Restaurantes(id_user=user.id, img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzBvQZv2QFuNasiNMHI3Z20Th9g2SNR4xmCg&usqp=CAU", tipo="RAP",nombre="Los perritos",hor_abierto="09:00",hor_cierre="10:00",personas=12) 
comp_rest = Restaurantes.query.filter_by(nombre="Los perritos").first()
if comp_rest is not None:
    pass
else:
    db.session.add(new_restaurant)
    db.session.commit()

