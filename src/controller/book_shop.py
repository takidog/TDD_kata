from typing import Dict, List
from uuid import UUID, uuid4


class BookShop:
    def __init__(self) -> None:
        self.items = {}
        self.pre_checkout_data: Dict["UUID", "Checkout"] = {}
        self.receipt_data = {}

    def add_items(self, name: str, price: int, quota: int) -> "Book":
        item = Book(name=name, price=price, quota=quota)
        self.items[item.id] = item
        return item

    def get_item(self, book_id: UUID) -> "Book":
        return self.items.get(book_id)

    def get_books_list(self) -> list:
        return self.items.values()

    def pre_checkout(self, item_list: List[Dict[str, UUID]]) -> "Checkout":
        for i in item_list:
            if isinstance(i["item_id"], str):
                i["item_id"] = UUID(i["item_id"])
            if i["item_id"] not in self.items:
                raise ValueError("Not found this items.")

        checkout = Checkout(
            item_list=[
                {"item": self.items[i["item_id"]], "quota": i["quota"]}
                for i in item_list
            ]
        )

        self.pre_checkout_data[checkout.checkout_id] = checkout

        return checkout

    def checkout(self, checkout_id: UUID) -> "Receipt":

        return self.pre_checkout_data.get(checkout_id).to_Receipt()


class Checkout:
    def __init__(self, item_list: List[Dict[str, "Book"]]) -> None:
        self.checkout_status = False
        self.checkout_id = uuid4()
        self.items = item_list
        self.price = self.get_price()

    def get_price(self):

        # merge same items
        _temp = {}
        for i in self.items:
            if _temp.get(i["item"].id):
                _temp[i["item"].id]["quota"] += i["quota"]
                continue
            _temp[i["item"].id] = i
        price = 0
        for item in _temp.values():
            price += item["item"].price * item["quota"]

        return price

    def to_Receipt(self):
        return Receipt(self.items)


class Receipt(Checkout):
    def __init__(self, item_list: List[Dict[str, "Book"]]) -> None:
        super().__init__(item_list)
        self.checkout_status = True
        self.receipt_id = uuid4()
        # self.price = super().get_price()  # re calc


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
