"""
Test Factory to make fake objects for testing
"""

import factory
from service.models import Order, Item
from factory.fuzzy import FuzzyDate, FuzzyInteger, FuzzyDecimal
from datetime import date
from decimal import Decimal


class OrderFactory(factory.Factory):
    """Creates fake Order that you don't have to pay"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Order

    id = factory.Sequence(lambda n: n)
    date = FuzzyDate(date(2008, 1, 1))
    status = FuzzyInteger(0, 2)
    amount = Decimal(0.0)
    address = factory.Faker("address")
    customer_id = factory.Sequence(lambda n: n)


class ItemFactory(factory.Factory):
    """Creates fake Item that you don't have to pay"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Item

    product_id = factory.Sequence(lambda n: n)
    order_id = factory.SelfAttribute("order.id")
    price = FuzzyDecimal(1.0)
    quantity = FuzzyInteger(1)
    order = factory.SubFactory(OrderFactory)
