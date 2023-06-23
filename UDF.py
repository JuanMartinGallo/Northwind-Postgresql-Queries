from sqlalchemy import (
    asc,
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Numeric,
    desc,
)
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func
import pandas as pd
import matplotlib.pyplot as plt

Base = declarative_base()
engine = create_engine("postgresql://postgres:root@127.0.0.1/northwind")
Session = sessionmaker(bind=engine)
session = Session()


class OrderDetails(Base):
    """Class to represent the order details table."""

    __tablename__ = "orderdetails"
    orderdetailid = Column(Integer, primary_key=True)
    orderid = Column(Integer, ForeignKey("orders.orderid"))
    productid = Column(Integer, ForeignKey("products.productid"))
    quantity = Column(Integer)


class Product(Base):
    __tablename__ = "products"

    productid = Column(Integer, primary_key=True)
    productname = Column(String)
    price = Column(Numeric)

    # GETTING THE 10 MOST PROFITABLE PRODUCTS

fst_query = (
    session.query(
        Product.productname,
        func.sum(Product.price * OrderDetails.quantity).label("Revenue"),
    )
    .join(OrderDetails, Product.productid == OrderDetails.productid)
    .group_by(Product.productid)
    .order_by(desc("Revenue"))
    .limit(10)
    .all()
)
top_products = pd.DataFrame(fst_query, columns=["ProductName", "Revenue"])
top_products["Revenue"] = pd.to_numeric(top_products["Revenue"])
top_products.plot(
    x="ProductName", y="Revenue", kind="bar", figsize=(10, 5), legend=False
)


plt.title("10 Most Profitable Products")
plt.xlabel("Products")
plt.ylabel("Revenue")
plt.xticks(rotation=90)
plt.show()


# GETTING THE 10 MOST EFFECTIVE EMPLOYEES
class Employee(Base):
    __tablename__ = "employees"

    employeeid = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)


class Order(Base):
    __tablename__ = "orders"

    orderid = Column(Integer, primary_key=True)
    employeeid = Column(Integer, ForeignKey("Employees.employeeid"))


snd_query = (
    session.query(
        (Employee.firstname + " " + Employee.lastname).label("Employee"),
        func.count(Order.orderid).label("Total"),
    )
    .join(Order, Employee.employeeid == Order.employeeid)
    .group_by(Employee.employeeid)
    .order_by(desc("Total"))
    .limit(10)
    .all()
)

top_employees = pd.DataFrame(snd_query, columns=["Employees", "Total"])

top_employees.plot(x="Employees", y="Total", kind="bar", figsize=(10, 5), legend=False)

plt.title("10 More Effective Employees")
plt.xlabel("Employees")
plt.ylabel("Total")
plt.xticks(rotation=45)
plt.show()

trd_query = (
    session.query(
        (Employee.firstname + " " + Employee.lastname).label("Employee"),
        func.count(Order.orderid).label("Total"),
    )
    .join(Order, Employee.employeeid == Order.employeeid)
    .group_by(Employee.employeeid)
    .order_by(asc("Total"))
    .limit(3)
    .all()
)

least_eff_employees = pd.DataFrame(snd_query, columns=["Employees", "Total"])

least_eff_employees.plot(
    x="Employees", y="Total", kind="bar", figsize=(10, 5), legend=False
)

plt.title("3 Least Efficient Employees")
plt.xlabel("Employees")
plt.ylabel("Total")
plt.xticks(rotation=45)
plt.show()

session.close()
engine.dispose()
