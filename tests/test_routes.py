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
from datetime import datetime
from unittest import TestCase

# from urllib.parse import quote_plus
from wsgi import app
from service.common import status
from service.models import db, Order
from .factories import OrderFactory, ItemFactory

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

    ############################################################
    # Utility function to bulk create orders
    ############################################################
    def _create_orders(self, count: int = 1) -> list:
        """Factory method to create orders in bulk"""
        orders = []
        for _ in range(count):
            test_order = OrderFactory()
            response = self.client.post(BASE_URL, json=test_order.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test order",
            )
            new_order = response.get_json()
            test_order.id = new_order["id"]
            orders.append(test_order)
        return orders

    def _create_items(self, order, count: int = 1) -> list:
        """Factory method to create items in bulk"""
        items = []
        item_url = "items"
        item_post_url = f"{BASE_URL}/{order.id}/{item_url}"

        for _ in range(count):
            test_item = ItemFactory(order=order)
            response = self.client.post(item_post_url, json=test_item.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test order",
            )
            items.append(test_item)
        return items

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # ----------------------------------------------------------
    # TEST HEALTH CHECK POINT
    # ----------------------------------------------------------
    def test_health_endpoint(self):
        """It should call the health endpoint"""
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

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

        # Check that the location header was correct
        response = self.client.get(location)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_order = response.get_json()
        # self.assertEqual(new_order["id"], test_order.id)
        self.assertEqual(new_order["date"], str(test_order.date))
        self.assertEqual(new_order["status"], test_order.status)
        self.assertEqual(new_order["amount"], test_order.amount)
        self.assertEqual(new_order["address"], test_order.address)
        self.assertEqual(new_order["customer_id"], test_order.customer_id)

    # ----------------------------------------------------------
    # TEST READ
    # ----------------------------------------------------------
    def test_get_order(self):
        """It should Read a single order"""
        # get the id of an order
        order = self._create_orders(1)[0]
        resp = self.client.get(
            f"{BASE_URL}/{order.id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["id"], order.id)

    def test_get_order_not_found(self):
        """It should not Read an Order that is not found"""
        resp = self.client.get(f"{BASE_URL}/-100")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

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
    # TEST DELETE
    # ----------------------------------------------------------
    def test_delete_order(self):
        """It should Delete an Order"""
        test_order = self._create_orders(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_order.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        # make sure they are deleted

        response = self.client.get(f"{BASE_URL}/{test_order.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_non_existing_order(self):
        """It should Delete an Order even if it doesn't exist"""
        response = self.client.delete(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)

    # ----------------------------------------------------------
    # TEST GET ALL ORDERS
    # ----------------------------------------------------------
    def test_get_all_orders(self):
        """It should retrieve all orders sorted by date"""
        self._create_orders(3)
        response = self.client.get("/orders")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(len(data), 3)
        dates = [order["date"] for order in data]
        self.assertEqual(dates, sorted(dates, reverse=True))

    def test_get_all_orders_empty(self):
        """Return empty list with status code 200 when there is no order"""
        response = self.client.get("/orders")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data, [])

    # ----------------------------------------------------------
    # TEST ACTIONS
    # ----------------------------------------------------------
    def test_cancel_an_order(self):
        """It should cancel an order"""
        orders = self._create_orders(10)
        available_orders = [order for order in orders if order.status != 0]
        order = available_orders[0]
        response = self.client.put(f"{BASE_URL}/{order.id}/cancel")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f"{BASE_URL}/{order.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        logging.debug("Response data: %s", data)
        self.assertEqual(data["status"], 0)

    def test_cancel_not_available(self):
        """It should not Cancel a Order that is not available"""
        orders = self._create_orders(100)
        unavailable_orders = [order for order in orders if order.status == 0]
        order = unavailable_orders[0]
        response = self.client.put(f"{BASE_URL}/{order.id}/cancel")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_deliver_an_order(self):
        """It should deliver an order"""
        orders = self._create_orders(10)
        available_orders = [order for order in orders if order.status != 0]
        order = available_orders[0]
        response = self.client.put(f"{BASE_URL}/{order.id}/deliver")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f"{BASE_URL}/{order.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        logging.debug("Response data: %s", data)
        self.assertEqual(data["status"], 3)

    def test_deliver_not_available(self):
        """It should not Deliver a Order that is not available"""
        orders = self._create_orders(100)
        unavailable_orders = [order for order in orders if order.status == 0]
        order = unavailable_orders[0]
        response = self.client.put(f"{BASE_URL}/{order.id}/deliver")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    # Don't need this part. - comment by TZ
    # @mock.patch("service.models.Order.query")
    # def test_get_all_orders_failure(self, mock_query):
    #     """It should return 500 when an exception occurs while retrieving orders"""
    #     mock_query.order_by.side_effect = Exception("Database Error")

    #     response = self.client.get("/orders")
    #     self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    #     data = response.get_json()
    #     self.assertIn("Failed to retrieve orders", data["error"])

    ######################################################################
    #  I T E M   T E S T   C A S E S
    ######################################################################

    # ----------------------------------------------------------
    # TEST CREATE AN ITEM
    # ----------------------------------------------------------
    def test_create_item(self):
        """It should Create a new item"""

        # Create an order to create an item
        order = self._create_orders(1)[0]

        # Create an Item
        test_item = ItemFactory(order=order)
        logging.debug("Test Item: %s", test_item.serialize())
        self.assertEqual(order.amount, 0)

        resp = self.client.post(
            f"{BASE_URL}/{order.id}/items",
            json=test_item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        logging.debug("Response Data: %s", resp.get_json())

        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_item = resp.get_json()

        self.assertEqual(new_item["order_id"], order.id)
        self.assertEqual(new_item["product_id"], test_item.product_id)

        # price need to be in the same type
        self.assertEqual(str(test_item.price), new_item["price"])
        self.assertEqual(new_item["quantity"], test_item.quantity)

        # Check that the location header was correct
        response = self.client.get(location, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # the returned value is a list of json
        new_item = response.get_json()
        self.assertEqual(new_item["order_id"], test_item.order_id)
        self.assertEqual(new_item["product_id"], test_item.product_id)
        self.assertEqual(new_item["price"], str(test_item.price))
        self.assertEqual(new_item["quantity"], test_item.quantity)

        # check the amount of the order changed accordingly
        resp = self.client.get(
            f"{BASE_URL}/{order.id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["amount"], float(test_item.amount()))

    def test_list_items(self):
        """It should Get a list of Items"""
        # add two addresses to order
        order = self._create_orders(1)[0]
        order.create()
        item_list = ItemFactory.create_batch(2)
        item_list[0].order = order
        item_list[1].order = order
        # Create item 1
        resp = self.client.post(
            f"{BASE_URL}/{order.id}/items", json=item_list[0].serialize()
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Create item 2
        resp = self.client.post(
            f"{BASE_URL}/{order.id}/items", json=item_list[1].serialize()
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # get the list back and make sure there are 2
        resp = self.client.get(f"{BASE_URL}/{order.id}/items")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        self.assertEqual(len(data), 2)

    def test_get_item(self):
        """It should Get an item from an order"""
        # create a known item
        order = self._create_orders(1)[0]
        item = ItemFactory(order=order)
        resp = self.client.post(
            f"{BASE_URL}/{order.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        item_id = data["product_id"]

        # retrieve it back
        resp = self.client.get(
            f"{BASE_URL}/{order.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["order_id"], order.id)
        self.assertEqual(data["product_id"], item.product_id)
        self.assertEqual(data["price"], str(item.price))
        self.assertEqual(data["quantity"], item.quantity)

    def test_update_item(self):
        """It should Update an item on an order"""
        # create a known item
        order = self._create_orders(1)[0]
        item = ItemFactory(order=order)
        resp = self.client.post(
            f"{BASE_URL}/{order.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        item_id = data["product_id"]
        data["price"] = 1
        data["quantity"] = 1

        # send the update back
        resp = self.client.put(
            f"{BASE_URL}/{order.id}/items/{item_id}",
            json=data,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # retrieve it back
        resp = self.client.get(
            f"{BASE_URL}/{order.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["product_id"], item_id)
        self.assertEqual(data["order_id"], order.id)
        self.assertEqual(int(data["price"]), 1)
        self.assertEqual(int(data["quantity"]), 1)

        # check the amount of the order changed accordingly
        resp = self.client.get(
            f"{BASE_URL}/{order.id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["amount"], 1)

    def test_delete_item(self):
        """It should Delete an Item"""
        order = self._create_orders(1)[0]
        item = ItemFactory(order=order)
        resp = self.client.post(
            f"{BASE_URL}/{order.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)
        item_id = data["product_id"]

        # send delete request
        resp = self.client.delete(
            f"{BASE_URL}/{order.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        # retrieve it back and make sure item is not there

        resp = self.client.get(
            f"{BASE_URL}/{order.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        # check the amount of the order changed accordingly
        resp = self.client.get(
            f"{BASE_URL}/{order.id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["amount"], 0)

    # ----------------------------------------------------------
    # TEST QUERY
    # ----------------------------------------------------------
    def test_query_orders_by_date(self):
        """It should query orders by date"""
        orders = self._create_orders(3)
        orders = Order.query.order_by(Order.date.desc()).all()
        resp = self.client.get(BASE_URL, query_string=f"date={orders[0].date}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        date = datetime.strptime(data[0]["date"], "%Y-%m-%d").date()
        self.assertEqual(date, orders[0].date)

    def test_query_orders_by_status(self):
        """It should query orders by status"""
        orders = self._create_orders(3)
        orders = Order.query.order_by(Order.date.desc()).all()
        resp = self.client.get(BASE_URL, query_string=f"status={orders[0].status}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        status_obj = int(data[0]["status"])
        self.assertEqual(status_obj, orders[0].status)

    def test_query_orders_by_customer_id(self):
        """It should query orders by customer_id"""
        orders = self._create_orders(3)
        orders = Order.query.order_by(Order.date.desc()).all()
        resp = self.client.get(
            BASE_URL, query_string=f"customer_id={orders[0].customer_id}"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        customer_id = int(data[0]["customer_id"])
        self.assertEqual(customer_id, orders[0].customer_id)

    def test_query_orders_by_address(self):
        """It should query orders by address"""
        orders = self._create_orders(3)
        orders = Order.query.order_by(Order.date.desc()).all()
        resp = self.client.get(BASE_URL, query_string=f"address={orders[0].address}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        address = data[0]["address"]
        self.assertEqual(address, orders[0].address)

    def test_query_items_by_price(self):
        """It should Query Items by Price"""
        # create an order
        orders = Order.all()
        self.assertEqual(orders, [])
        order = OrderFactory()
        order.create()
        self.assertIsNotNone(order.id)
        orders = Order.all()
        self.assertEqual(len(orders), 1)

        # create some items
        items = self._create_items(order, 5)
        self.assertEqual(len(items), 5)
        test_price = items[0].price
        price_count = len([item for item in items if item.price == test_price])
        response = self.client.get(
            f"{BASE_URL}/{order.id}/items", query_string={"price": test_price}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), price_count)
        # check the data just to be sure
        for item in data:
            self.assertEqual(item["price"], str(test_price))

    def test_query_items_by_quantity(self):
        """It should Query Items by Quantity"""
        # create an order
        orders = Order.all()
        self.assertEqual(orders, [])
        order = OrderFactory()
        order.create()
        self.assertIsNotNone(order.id)
        orders = Order.all()
        self.assertEqual(len(orders), 1)

        # create some items
        items = self._create_items(order, 5)
        self.assertEqual(len(items), 5)
        test_quantity = items[0].quantity
        quantity_count = len([item for item in items if item.quantity == test_quantity])
        response = self.client.get(
            f"{BASE_URL}/{order.id}/items", query_string={"quantity": test_quantity}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), quantity_count)
        # check the data just to be sure
        for item in data:
            self.assertEqual(item["quantity"], test_quantity)


######################################################################
#  T E S T   S A D   P A T H S
######################################################################
class TestSadPaths(TestCase):
    """Test REST Exception Handling"""

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()

    def test_method_not_allowed(self):
        """It should not allow update without a order id"""
        response = self.client.put(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_order_no_data(self):
        """It should not Create an Order with missing data"""
        response = self.client.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_no_content_type(self):
        """It should not Create an Order with no content type"""
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_order_wrong_content_type(self):
        """It should not Create an Order with wrong content type"""
        order = OrderFactory()
        resp = self.client.post(
            BASE_URL, json=order.serialize(), content_type="test/html"
        )
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_order_bad_available(self):
        """It should not Create an Order with bad available data"""
        test_order = OrderFactory()
        logging.debug(test_order)
        # change available to a string
        test_order.status = "a string"
        response = self.client.post(BASE_URL, json=test_order.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_items_not_available(self):
        """It should not Get items if order does not exist"""
        resp = self.client.get(
            f"{BASE_URL}/{-100}/items/{-100}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_items_not_available(self):
        """It should not Update items if order does not exist"""
        resp = self.client.put(
            f"{BASE_URL}/{-100}/items/{-100}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_orders_not_available(self):
        """It should not Update an order if order does not exist"""
        resp = self.client.put(
            f"{BASE_URL}/{100}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_items_not_available(self):
        """It should not Create items if order does not exist"""
        resp = self.client.post(
            f"{BASE_URL}/{100}/items",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
