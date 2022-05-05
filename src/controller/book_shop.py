from uuid import UUID, uuid4


class BookShop:
    def __init__(self) -> None:
        self.items = {}

    def add_items(self, name: str, price: int, quota: int) -> "Book":
        item = Book(name=name, price=price, quota=quota)
        self.items[item.id] = item
        return item

    def get_item(self, book_id: UUID):
        return self.items.get(book_id)


class Book:
    def __init__(self, name: str, price: int, quota: int) -> None:
        self.id = uuid4()
        self.name = name
        self.price = price
        self.quota = quota

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quota": self.quota,
        }
