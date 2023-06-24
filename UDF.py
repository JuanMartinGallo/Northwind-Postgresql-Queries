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

#Connection to Northwind DB
Base = declarative_base()
engine = create_engine("postgresql://postgres:root@127.0.0.1/northwind")
Session = sessionmaker(bind=engine)
session = Session()

############################### Classes ###############################
class OrderDetails(Base):
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


class Employee(Base):
    __tablename__ = "employees"

    employeeid = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)


class Order(Base):
    __tablename__ = "orders"

    orderid = Column(Integer, primary_key=True)
    employeeid = Column(Integer, ForeignKey("Employees.employeeid"))

############################### FUNCTIONS ###############################
def generate_graphs(x, y, title, xlabel, ylabel, query, xTicks):
    allowed_types = [
        "line",
        "bar",
        "barh",
        "hist",
        "box",
        "kde",
        "density",
        "area",
        "pie",
        "scatter",
        "hexbin",
    ]

    print("Select what kind of graph do you want:")
    for i, t in enumerate(allowed_types):
        print(f"{i+1}. {t}")
    while True:
        choice = input("Enter a number: ")
        try:
            choice = int(choice)
            if choice >= 1 and choice <= len(allowed_types):
                graphK = allowed_types[choice - 1]
                break
            else:
                print("\rInvalid choice. Please enter a number.")
        except ValueError:
            print("\rInvalid input. Please enter a number.")

    result = pd.DataFrame(query, columns=[x, y])

    if not pd.api.types.is_numeric_dtype(result[y]):
        result[y] = pd.to_numeric(result[y])

    result.plot(x=x, y=y, kind=graphK, figsize=(10, 5), legend=False)  # type: ignore

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=xTicks)
    plt.show()
    
############################### Queries ###############################
# GETTING THE 10 MOST PROFITABLE PRODUCTS
try:
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

    generate_graphs(
        "ProductName",
        "Revenue",
        "10 Most Profitable Products",
        "Products",
        "Revenue",
        fst_query,
        90,
    )

except Exception as e:
    print(f"An error occurred while executing the query: {str(e)}")
    session.rollback()
finally:
    session.close()
    engine.dispose()

# GETTING THE 10 MOST EFFECTIVE EMPLOYEES
try:
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

    generate_graphs(
        "Employee",
        "Total",
        "10 More Effective Employees",
        "Employees",
        "Total",
        snd_query,
        45,
    )

except Exception as e:
    print(f"An error occurred while executing the query: {str(e)}")
    session.rollback()
finally:
    session.close()
    engine.dispose()

# GETTING THE 3 LEAST EFFICIENT EMPLOYEES
try:
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

    generate_graphs(
        "Employee",
        "Total",
        "3 Least Effective Employees",
        "Employees",
        "Total",
        trd_query,
        45,
    )

except Exception as e:
    print(f"An error occurred while executing the query: {str(e)}")
    session.rollback()
finally:
    session.close()
    engine.dispose()


