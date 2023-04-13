from flask_login import UserMixin
from sqlalchemy import Table, Column, Integer, String, ForeignKey

from RugWebsite.__init__ import db, meta, engine

def createAll():
    meta.create_all(engine)
def dropAll():
    meta.drop_all(engine, checkfirst=True)


# SQLAlchemy Tables
USERS_Table = Table("Users", meta,
                        Column("userID", Integer, primary_key=True, autoincrement=True, nullable=True),
                        Column("username", String, unique=True, nullable=False),
                        Column("password", String, nullable=False),
                        Column("email", String, nullable=True))

ORDERS_Table = Table("Orders", meta,
                        Column("orderID", Integer, primary_key=True, autoincrement=True, nullable=True),
                        Column("userID", String, ForeignKey("Users.userID")))

PRODUCTS_Table = Table("Products", meta,
                        Column("productID", Integer, primary_key=True, autoincrement=True, nullable=True),
                        Column("productName", String, unique=True, nullable=False),
                        Column("productPrice", Integer, nullable=False))

CARTS_Table = Table("Carts", meta,
                        Column("cartID", Integer, primary_key=True, autoincrement=True, nullable=True),
                        Column("userID", String, ForeignKey("Users.userID"), nullable=False),
                        Column("productID", String, ForeignKey("Products.productID")),
                        Column("quantity", Integer))

CARTITEMS_Table = Table("CartItems", meta,
                        Column("cartItemID", Integer, primary_key=True, autoincrement=True, nullable=True),
                        Column("cartID", String, ForeignKey("Carts.cartID"), nullable=False),
                        Column("productID", String, ForeignKey("Products.productID"), nullable=False),
                        Column("quantity", Integer))

# Python classes - Each class corresponds to one Table
class Users(db.Model, UserMixin):
    __tablename__ = "Users"
    __table_args__ = {'extend_existing': True}

    userID = db.Column(db.Integer(), primary_key=True, nullable=True, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(40), nullable=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

class Orders(db.Model):
    __tablename__ = "Orders"
    __table_args__ = {'extend_existing': True}

    orderID = db.Column(db.Integer(), primary_key=True, nullable=True, unique=True)
    userID = db.Column(db.Integer(), db.ForeignKey("Users.userID"))

    def __init__(self, orderid, userid):
        self.orderID = orderid
        self.userID = userid

class Products(db.Model):
    __tablename__ = "Products"
    __table_args__ = {"extend_existing": True}

    productID = db.Column(db.Integer(), primary_key=True, nullable=True, unique=True)
    productName = db.Column(db.String(30), nullable=False, unique=True)
    productPrice = db.Column(db.Float())

    def __init__(self, productid, productname, productprice):
        self.productID = productid
        self.productName = productname
        self.productPrice = productprice

class Carts(db.Model):
    __tablename__ = "Carts"
    __table_args__ = {"extend_existing": True}

    cartID = db.Column(db.Integer(), primary_key=True, nullable=True, unique=True)
    userID = db.Column(db.Integer(), db.ForeignKey("Users.userID"))

    def __init__(self, cartid, userid, quantity):
        self.cartID = cartid
        self.userID = userid
        self.quantity = quantity

class CartItem(db.Model):
    __tablename__ = "CartItems"
    __table_args__ = {"extend_existing": True}

    cartItemID = db.Column(db.Integer(), primary_key=True, nullable=True, unique=True)
    cartID = db.Column(db.Integer(), db.ForeignKey("Cart.cartID"))
    productID = db.Column(db.Integer(), db.ForeignKey("Product.productID"))
    quantity = db.Column(db.Integer(), nullable=False)

    def __init__(self, cartitemid, cartid, productid):
        self.cartItemID = cartitemid
        self.cartID = cartid
        self.productID = productid
