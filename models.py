import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    publisher_id = sq.Column(sq.Integer, primary_key=True)
    name_publisher = sq.Column(sq.String(length=100), nullable=False)

    def __repr__(self):
        return f"{self.publisher_id}, {self.name_publisher}"


class Book(Base):
    __tablename__ = "book"

    book_id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=200), nullable=False)
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey("publisher.publisher_id", ondelete="CASCADE"), nullable=False)

    publisher = relationship(Publisher, backref="book")

    def __repr__(self):
        return f"{self.book_id}, {self.title}, {self.publisher_id}"


class Shop(Base):
    __tablename__ = "shop"

    shop_id = sq.Column(sq.Integer, primary_key=True)
    name_shop = sq.Column(sq.String(length=100), nullable=False)

    def __repr__(self):
        return f"{self.shop_id}, {self.name_shop}"


class Stock(Base):
    __tablename__ = "stock"

    stock_id = sq.Column(sq.Integer, primary_key=True)
    count = sq.Column(sq.Integer, default=0)
    book_id = sq.Column(sq.Integer, sq.ForeignKey("book.book_id", ondelete="CASCADE"), nullable=False)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey("shop.shop_id", ondelete="CASCADE"), nullable=False)

    book = relationship(Book, backref="stock_book")
    shop = relationship(Shop, backref="stock_shop")

    def __repr__(self):
        return f"{self.stock_id}, {self.count}, {self.book_id}, {self.shop_id}"


class Sale(Base):
    __tablename__ = "sale"

    sale_id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.NUMERIC(8, 2), nullable=False)
    date_sale = sq.Column(sq.DateTime, default=datetime.now)
    count = sq.Column(sq.Integer, default=0)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey("stock.stock_id", ondelete="CASCADE"), nullable=False)

    stock = relationship(Stock, backref="sale")

    def __repr__(self):
        return f"{self.sale_id}, {self.price}, {self.date_sale}, {self.count}, {self.stock_id}"
