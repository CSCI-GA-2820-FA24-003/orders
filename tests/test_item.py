######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Test cases for Item Model
"""

# pylint: disable=duplicate-code
import os
import logging
from unittest import TestCase
from wsgi import app
from service.models import Order, Item, db
from .factories import OrderFactory, ItemFactory
from service.models.persistent_base import DataValidationError

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  I T E M   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestItem(TestCase):
    """Test Cases for Item Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Order).delete()  # clean up the last tests
        db.session.query(Item).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_item(self):
        """It should create an Item associate with an Order and add it to the database"""
        orders = Order.all()
        self.assertEqual(orders, [])
        order = OrderFactory()
        item = ItemFactory(order=order)
        order.amount = order.amount + item.amount()
        order.create()
        self.assertIsNotNone(order.id)
        orders = Order.all()
        self.assertEqual(len(orders), 1)

        new_order = Order.find(order.id)
        self.assertEqual(new_order.id, item.order_id)

        new_item = ItemFactory(order=order)
        order.amount += new_item.amount()
        order.update()

        new_order = Order.find(order.id)
        self.assertEqual(new_order.id, new_item.order_id)
        self.assertEqual(
            new_order.amount,
            item.amount() + new_item.amount(),
        )

    def test_update_order_item(self):
        """It should Update an item in an order"""
        orders = Order.all()
        self.assertEqual(orders, [])

        order = OrderFactory()
        item = ItemFactory(order=order)
        order.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(order.id)
        orders = Order.all()
        self.assertEqual(len(orders), 1)

        # Fetch it back
        order = Order.find(order.id)
        old_item = Item.find_by_product_id(order.id, item.product_id)
        print("%r", old_item)
        self.assertEqual(old_item.quantity, item.quantity)
        # Change the quantity of item and update the amount in order
        old_item_quantity = old_item.quantity
        old_item.quantity = old_item_quantity + 10
        old_order_amount = order.amount
        new_order_amount = old_order_amount + 10 * old_item.price
        Order.update_amount(order.id, new_order_amount)

        # Fetch it back again
        order = Order.find(order.id)
        item = Item.find_by_product_id(order.id, old_item.product_id)
        self.assertEqual(item.quantity, old_item_quantity + 10)
        self.assertEqual(order.amount, new_order_amount)

    def test_delete_order_item(self):
        """It should Delete an item of an order"""
        orders = Order.all()
        self.assertEqual(orders, [])

        order = OrderFactory()
        item = ItemFactory(order=order)
        order.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(order.id)
        orders = Order.all()
        self.assertEqual(len(orders), 1)

        # Fetch it back
        order = Order.find(order.id)
        item = Item.find_by_product_id(order.id, item.product_id)
        delete_item_id = item.product_id
        # amount that order should subtract
        amount_of_item = item.price * item.quantity
        order_new_amount = order.amount - amount_of_item

        item.delete()
        Order.update_amount(order.id, order_new_amount)

        # Fetch it back again
        order = Order.find(order.id)
        self.assertEqual(order.amount, order_new_amount)
        item = Item.find_by_product_id(order.id, delete_item_id)
        self.assertEqual(item, None)

    def test_serialize_an_item(self):
        """It should serialize an Item"""
        order = OrderFactory()
        item = ItemFactory(order=order)
        serial_item = item.serialize()
        self.assertEqual(serial_item["order_id"], item.order_id)
        self.assertEqual(serial_item["product_id"], item.product_id)
        self.assertEqual(serial_item["quantity"], item.quantity)
        self.assertEqual(serial_item["price"], item.price)

    def test_deserialize_an_item(self):
        """It should deserialize an Item"""
        order = OrderFactory()
        item = ItemFactory(order=order)
        order.create()
        item.create()
        new_item = Item()
        new_item.deserialize(item.serialize())
        self.assertEqual(item.product_id, new_item.product_id)
        self.assertEqual(item.price, new_item.price)
        self.assertEqual(item.quantity, new_item.quantity)

    def test_deserialize_with_key_error(self):
        """It should not Deserialize an item with a KeyError"""
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, {})

    def test_deserialize_with_type_error(self):
        """It should not Deserialize an item with a TypeError"""
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, [])
