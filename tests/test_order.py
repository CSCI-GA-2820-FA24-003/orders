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
Test cases for Order Model
"""

# pylint: disable=duplicate-code
import os
import logging
from unittest import TestCase
from wsgi import app
from service.models import Order, db
from .factories import OrderFactory
from .factories import ItemFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  O R D E R   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestOrder(TestCase):
    """Test Cases for Order Model"""

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
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_order(self):
        """It should create an order"""
        order = OrderFactory()
        order.create()
        self.assertIsNotNone(order.id)
        found = Order.all()
        self.assertEqual(len(found), 1)
        data = Order.find(order.id)
        self.assertEqual(data.id, order.id)
        self.assertEqual(data.date, order.date)
        self.assertEqual(data.status, order.status)
        self.assertEqual(data.amount, order.amount)
        self.assertEqual(data.address, order.address)
        self.assertEqual(data.customer_id, order.customer_id)


    def test_update_a_order(self):
        """It should Update a Order"""
        order = OrderFactory()
        logging.debug(order)
        order.id = None
        order.create()
        logging.debug(order)
        self.assertIsNotNone(order.id)
        # Change it an save it
        order.date = "2024-10-12"
        order.status = 1
        order.amount = 100
        order.address = "abc"
        order.customer_id = 123
        original_id = order.id
        order.update()
        self.assertEqual(order.id, original_id)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        orders = Order.all()
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].id, original_id)
        updated_date = orders[0].date.strftime('%Y-%m-%d')
        self.assertEqual(updated_date, "2024-10-12")
        self.assertEqual(orders[0].status, 1)
        self.assertEqual(orders[0].amount, 100)
        self.assertEqual(orders[0].address, "abc")
        self.assertEqual(orders[0].customer_id, 123)

    def test_list_all_orders(self):
        """It should List All Orders"""
        # Create a couple of orders
        order1 = OrderFactory()
        order1.create()
        order2 = OrderFactory()
        order2.create()

        # Retrieve all orders
        orders = Order.all()
        self.assertEqual(len(orders), 2)
        self.assertIn(order1, orders)
        self.assertIn(order2, orders)






    # Todo: Add your test cases here...

