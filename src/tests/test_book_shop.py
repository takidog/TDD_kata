from controller.book_shop import BookShop, Book
from uuid import UUID


def test_product_listing():
    shop = BookShop()

    book_item = shop.add_items(name="Potter Part.1", price=100, quota=10)

    assert book_item.name == "Potter Part.1"

    assert book_item.price == 100

    assert book_item.quota == 10

    assert shop.get_item(book_id=book_item.id).id == book_item.id


def test_book_model():
    book = Book(name="test", price=300, quota=10)
    assert book.name == "test"
    assert book.price == 300
    assert book.quota == 10

    assert isinstance(book.id, UUID)

    book_dict = book.to_dict()
    assert isinstance(book_dict, dict)

    required_keys = ["id", "name", "price", "quota"]
    assert all([k in book_dict.keys() for k in required_keys])


def test_buy_one():
    shop = BookShop()

    book_item = shop.add_items(name="Potter Part.1", price=100, quota=10)

    pre_checkout = shop.pre_checkout(
        item_list=[
            {"item_id": book_item.id, "quota": 1},
        ],
    )

    assert pre_checkout.price == 100
    assert len(pre_checkout.items) == 1
    assert isinstance(pre_checkout.checkout_id, UUID)

    receipt = shop.checkout(checkout_id=pre_checkout.checkout_id)

    assert receipt.price == 100
    assert len(receipt.items) == 1
    assert isinstance(receipt.receipt_id, UUID)
    assert isinstance(receipt.checkout_id, UUID)


def test_buy_many():
    pass
