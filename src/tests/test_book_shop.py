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
    shop = BookShop()

    book_item_p1 = shop.add_items(name="Potter Part.1", price=100, quota=10)
    book_item_p2 = shop.add_items(name="Potter Part.2", price=100, quota=3)
    book_item_p3 = shop.add_items(name="Potter Part.3", price=100, quota=5)
    book_item_p4 = shop.add_items(name="Potter Part.4", price=100, quota=7)
    book_item_p5 = shop.add_items(name="Potter Part.5", price=100, quota=8)

    pre_checkout = shop.pre_checkout(
        item_list=[
            {"item_id": book_item_p1.id, "quota": 5},
            {"item_id": book_item_p2.id, "quota": 2},
            {"item_id": book_item_p4.id, "quota": 2},
        ],
    )

    assert pre_checkout.price == 100 * 9 * 0.9
    assert len(pre_checkout.items) == 3
    assert isinstance(pre_checkout.checkout_id, UUID)

    receipt = shop.checkout(checkout_id=pre_checkout.checkout_id)

    assert receipt.price == 100 * 9 * 0.9
    assert len(receipt.items) == 3
    assert isinstance(receipt.receipt_id, UUID)
    assert isinstance(receipt.checkout_id, UUID)

    # over quota

    pre_checkout = shop.pre_checkout(
        item_list=[
            {"item_id": book_item_p3.id, "quota": 99},
        ],
    )

    assert pre_checkout.price == 100 * 99
    assert len(pre_checkout.items) == 1
    assert isinstance(pre_checkout.checkout_id, UUID)
    try:
        receipt = shop.checkout(checkout_id=pre_checkout.checkout_id)
    except ValueError as e:
        assert e.args[0] == "Quota not enough"

    pre_checkout = shop.pre_checkout(
        item_list=[
            {"item_id": book_item_p1.id, "quota": 4},
            {"item_id": book_item_p2.id, "quota": 1},
            {"item_id": book_item_p3.id, "quota": 1},
            {"item_id": book_item_p4.id, "quota": 1},
            {"item_id": str(book_item_p5.id), "quota": 1},
        ],
    )

    assert pre_checkout.price == 100 * 8 * 0.75
    assert len(pre_checkout.items) == 5
    assert isinstance(pre_checkout.checkout_id, UUID)

    receipt = shop.checkout(checkout_id=pre_checkout.checkout_id)

    assert receipt.price == 100 * 8 * 0.75
    assert len(receipt.items) == 5
    assert isinstance(receipt.receipt_id, UUID)
    assert isinstance(receipt.checkout_id, UUID)
