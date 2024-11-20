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
Order Steps

Steps file for Order.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
from compare3 import expect
from behave import given  # pylint: disable=no-name-in-module

# HTTP Return Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204

WAIT_TIMEOUT = 60


@given("the following orders")
def step_impl(context):
    """Delete all Orders and load new ones"""

    # Get a list all of the orders
    rest_endpoint = f"{context.base_url}/orders"
    context.resp = requests.get(rest_endpoint, timeout=WAIT_TIMEOUT)
    expect(context.resp.status_code).equal_to(HTTP_200_OK)
    # and delete them one by one
    for order in context.resp.json():
        context.resp = requests.delete(
            f"{rest_endpoint}/{order['id']}", timeout=WAIT_TIMEOUT
        )
        expect(context.resp.status_code).equal_to(HTTP_204_NO_CONTENT)

    # load the database with new orders
    for row in context.table:
        payload = {
            "amount": row["amount"],
            "address": row["address"],
            "status": row["status"],
            "customer_id": row["customer_id"],
            "date": row["date"],
        }
        context.resp = requests.post(rest_endpoint, json=payload, timeout=WAIT_TIMEOUT)
        expect(context.resp.status_code).equal_to(HTTP_201_CREATED)


@given("the following items")
def step_impl(context):
    """Add items to existing orders"""

    # Ensure orders exist
    rest_endpoint = f"{context.base_url}/orders"
    context.resp = requests.get(rest_endpoint, timeout=WAIT_TIMEOUT)
    assert context.resp.status_code == HTTP_200_OK, f"Error: {context.resp.text}"
    existing_orders = [order["id"] for order in context.resp.json()]

    # Add items to orders
    for row in context.table:
        order_id = int(row["order_id"])
        assert order_id in existing_orders, f"Order {order_id} does not exist."
        payload = {
            "order_id": order_id,
            "product_id": int(row["product_id"]),
            "price": float(row["price"]),
            "quantity": int(row["quantity"]),
        }
        endpoint = f"{rest_endpoint}/{order_id}/items"
        print(f"Sending payload to {endpoint}: {payload}")
        context.resp = requests.post(endpoint, json=payload, timeout=WAIT_TIMEOUT)
        print(f"Response: {context.resp.status_code}, Body: {context.resp.text}")
        assert (
            context.resp.status_code == HTTP_201_CREATED
        ), f"Error: {context.resp.text}"

        response_data = context.resp.json()
        assert response_data["order_id"] == payload["order_id"]
        assert response_data["product_id"] == payload["product_id"]
        assert (
            float(response_data["price"]) == payload["price"]
        ), f"Expected price {payload['price']}, got {response_data['price']}"
        assert response_data["quantity"] == payload["quantity"]
