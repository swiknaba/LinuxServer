'''
in case of error: delete the old database file first
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Base, Categorie, Item, User

engine = create_engine('sqlite:///productcatalog.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

#create some Categories
cat1 = Categorie(name="Soccer")
session.add(cat1)
session.commit()

cat2 = Categorie(name="Basketball")
session.add(cat2)
session.commit()

cat3 = Categorie(name="Baseball")
session.add(cat3)
session.commit()

cat4 = Categorie(name="Frisbee")
session.add(cat4)
session.commit()

cat5 = Categorie(name="Snowboarding")
session.add(cat5)
session.commit()

cat6 = Categorie(name="MMA")
session.add(cat6)
session.commit()

cat7 = Categorie(name="Skiing")
session.add(cat7)
session.commit()


#create a user
usr1 = User(name="Lud", email="ludwigreinmiedl@gmail.com")
session.add(usr1)
session.commit()

#create some items
item1 = Item(name="A round leather ball", slug="round-leather-ball",
             categorie=cat1, description="This fine ball is made from leather",
             user=usr1)
session.add(item1)
session.commit()

item2 = Item(name="A T-Shirt", slug="t-shirt",
             categorie=cat1, description="This fine T-Shirt is cool",
             user=usr1)
session.add(item2)
session.commit()


print("added some categories and itmes, have fun with it!")
