import json
import os.path
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models import Base, Publisher, Book, Sale, Shop, Stock


def create_session(user, password, host, port, db_name):
    try:
        DSN = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
        engine = sqlalchemy.create_engine(DSN)
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
    except Exception as ex_sess:
        print(f"Ошибка при подключении сессии. {ex_sess}")


def get_data_from_json(file_name):
    try:
        with open(file_name) as file:
            data = json.load(file)
    except Exception as ex_f:
        print(f"Ошибка при открытии файла. {ex_f}")
        return
    return data


def fill_in_tables(db_session, info):
    try:
        for item in info:
            if item["model"] == "publisher":
                publisher = Publisher(publisher_id=item["pk"], name_publisher=item["fields"]["name"])
                db_session.add(publisher)
            if item["model"] == "book":
                book = Book(book_id=item["pk"], title=item["fields"]["title"],
                            publisher_id=item["fields"]["id_publisher"])
                db_session.add(book)
            if item["model"] == "shop":
                shop = Shop(shop_id=item["pk"], name_shop=item["fields"]["name"])
                db_session.add(shop)
            if item["model"] == "stock":
                stock = Stock(stock_id=item["pk"], shop_id=item["fields"]["id_shop"],
                              book_id=item["fields"]["id_book"], count=item["fields"]["count"])
                db_session.add(stock)
            if item["model"] == "sale":
                sale = Sale(sale_id=item["pk"], price=item["fields"]["price"],
                            date_sale=item["fields"]["date_sale"], count=item["fields"]["count"],
                            stock_id=item["fields"]["id_stock"])
                db_session.add(sale)
            db_session.commit()
    except Exception as ex_fill:
        print(f"Что-то пошла не так при заполнении таблиц. {ex_fill}")


def get_info_about_publisher(db_sess, name_publisher):
    if "'" in name_publisher:
        name_publisher = name_publisher.replace("'", "\u2019")
    if name_publisher not in ("O’Reilly", "Pearson", "Microsoft Press", "No starch press"):
        print("Искомого издательства в таблице нет!!!")
    try:
        result = db_sess.query(Publisher, Book, Stock, Sale, Shop). \
            join(Book, Publisher.publisher_id == Book.publisher_id). \
            join(Stock, Book.book_id == Stock.book_id). \
            join(Sale, Sale.stock_id == Stock.stock_id). \
            join(Shop, Stock.shop_id == Shop.shop_id).filter(Publisher.name_publisher == name_publisher).all()
        print("название книг".ljust(45), "название магазины, в котором была куплена книга".ljust(50),
              "стоимость покупки".ljust(20), "дата покупки")
        for publisher, book, stock, sale, shop in result:
            print(book.title.ljust(45), shop.name_shop.ljust(50),
                  str(sale.price * sale.count).ljust(20), sale.date_sale.strftime("%d-%m-%Y"))

    except Exception as ex_query:
        print(f"Ошибка при извлечении данных из таблиц. {ex_query}")


if __name__ == "__main__":
    dotenv_path = "config.env"
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    user_postgresql = os.getenv("USER")
    password_postgresql = os.getenv("PASSWORD")
    localhost = os.getenv("HOST")
    port_postgresql = os.getenv("PORT")
    name_db = os.getenv("DB_NAME")
    data_from_json = get_data_from_json("tests_data.json")
    sess = create_session(user=user_postgresql,
                          password=password_postgresql,
                          host=localhost,
                          port=port_postgresql,
                          db_name=name_db)
    fill_in_tables(sess, data_from_json)
    publisher_name = input("Введите название издательства: ")
    get_info_about_publisher(sess, publisher_name)
    if sess:
        sess.close()
