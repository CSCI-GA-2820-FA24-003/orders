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
TestYourResourceModel API Service Test Suite
"""

# pylint: disable=duplicate-code
import os
import logging
from unittest import TestCase
from wsgi import app
from service.common import status
from service.models import db, Order
from .factories import OrderFactory
from .factories import ItemFactory
from datetime import datetime

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/orders"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class OrderTestSuite(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Order).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # Todo: Add your test cases here...
    # ----------------------------------------------------------
    # TEST CREATE
    # ----------------------------------------------------------
    def test_create_order(self):
        """It should Create a new Order"""
        test_order = OrderFactory()
        logging.debug("Test Order: %s", test_order.serialize())
        response = self.client.post(BASE_URL, json=test_order.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_order = response.get_json()

        # self.assertEqual(new_order["id"], test_order.id)
        new_order_date = datetime.strptime(new_order["date"], "%Y-%m-%d").date()
        self.assertEqual(new_order_date, test_order.date)
        self.assertEqual(new_order["status"], test_order.status)
        self.assertEqual(new_order["amount"], test_order.amount)
        self.assertEqual(new_order["address"], test_order.address)
        self.assertEqual(new_order["customer_id"], test_order.customer_id)

        #TODO: uncomment this code when get_order is implemented

        # Check that the location header was correct
        # response = self.client.get(location)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # new_order = response.get_json()
        # self.assertEqual(new_order["id"], test_order.id)
        # self.assertEqual(new_order["date"], test_order.date)
        # self.assertEqual(new_order["status"], test_order.status)
        # self.assertEqual(new_order["amount"], test_order.amount)
        # self.assertEqual(new_order["address"], test_order.address)
        # self.assertEqual(new_order["customer_id"], test_order.customer_id)

    # ----------------------------------------------------------
    # TEST UPDATE
    # ----------------------------------------------------------
    def test_update_order(self):
        """It should Update an existing Order"""
        # create a order to update
        test_order = OrderFactory()
        response = self.client.post(BASE_URL, json=test_order.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the order
        new_order = response.get_json()
        logging.debug(new_order)
        
        new_order["date"] = "2024-10-12"
        new_order["status"] = 0
        new_order["amount"] = 0
        new_order["address"] = "unknown"
        new_order["customer_id"] = 0
        response = self.client.put(f"{BASE_URL}/{new_order['id']}", json=new_order)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_order = response.get_json()
        self.assertEqual(updated_order["date"], "2024-10-12")
        self.assertEqual(updated_order["status"], 0)
        self.assertEqual(updated_order["amount"], 0)
        self.assertEqual(updated_order["address"], "unknown")
        self.assertEqual(updated_order["customer_id"], 0)


    # ----------------------------------------------------------
    # TEST CREATE AN ITEM
    # ----------------------------------------------------------
    def test_create_item(self):
        """It should Create a new item"""

        # Create an order to create an item
        test_order = OrderFactory()
        response = self.client.post(BASE_URL, json=test_order.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_order = response.get_json()

        test_item = test_item = ItemFactory(order_id=new_order['id'])

        logging.debug("Test Item: %s", test_item.serialize())

        ITEM_URL = "items"
        ITEM_POST_URL = f"{BASE_URL}/{new_order['id']}/{ITEM_URL}"
        test_response = self.client.post(ITEM_POST_URL, json=test_item.serialize())
        self.assertEqual(test_response.status_code, status.HTTP_201_CREATED)
        logging.debug("Response Data: %s", test_response.get_json())


        # Make sure location header is set
        location = test_response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_item = test_response.get_json()

        self.assertEqual(new_item["order_id"], test_item.order_id)
        self.assertEqual(new_item["product_id"], test_item.product_id)

        # price need to be in the same type
        self.assertEqual(str(test_item.price), new_item["price"])
        self.assertEqual(new_item["quantity"], test_item.quantity)

        #TODO: uncomment this code when get_item is implemented

        # Check that the location header was correct
        # response = self.client.get(location)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # new_item = response.get_json()
        # self.assertEqual(new_item["order_id"], test_item.order_id)
        # self.assertEqual(new_item["product_id"], test_item.product_id)
        # self.assertEqual(new_item["price"], test_item.price)
        # self.assertEqual(new_item["quantity"], test_item.quantity)