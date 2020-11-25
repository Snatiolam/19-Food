from app import *

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
