from controller.book_shop import BookShop


def test_product_listing():
    shop = BookShop()

    book_item = shop.add_items(name="Potter Part.1", price=100, quota=10)

    assert book_item.name == "Potter Part.1"

    assert book_item.price == 100

    assert book_item.quota == 10

    assert shop.get_items(book_id=book_item.id) == book_item.id
