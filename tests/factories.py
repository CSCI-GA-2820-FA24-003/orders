"""
Test Factory to make fake objects for testing
"""

from datetime import date
from decimal import Decimal
import factory
from factory.fuzzy import FuzzyDate, FuzzyInteger, FuzzyDecimal
from service.models import Order, Item


class OrderFactory(factory.Factory):
    """Creates fake Order that you don't have to pay"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Order

    id = factory.Sequence(lambda n: n)
    date = FuzzyDate(date(2008, 1, 1))
    status = FuzzyInteger(0, 3)
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
    price = FuzzyDecimal(1.0, 10.0)
    quantity = FuzzyInteger(1, 10)
    order = factory.SubFactory(OrderFactory)
