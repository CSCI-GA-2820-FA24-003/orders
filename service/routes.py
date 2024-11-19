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
YourResourceModel Service

This service implements a REST API that allows you to Create, Read, Update
and Delete YourResourceModel
"""

from datetime import datetime
from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import Order
from service.models import Item
from service.common import status  # HTTP Status Codes

######################################################################
# HEALTH CHECK
######################################################################
@app.route("/health")
def health_check():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Base URL for our service"""
    return app.send_static_file("index.html")


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
# CREATE A NEW ORDER
######################################################################
@app.route("/orders", methods=["POST"])
def create_orders():
    """
    Create an Order
    This endpoint will create an Order based the data in the body that is posted
    """
    app.logger.info("Request to Create an Order...")
    check_content_type("application/json")

    order = Order()
    # Get the data from the request and deserialize it
    data = request.get_json()
    app.logger.info("Processing: %s", data)
    order.deserialize(data)

    # Save the new Order to the database
    order.create()
    app.logger.info("Order with new id [%s] saved!", order.id)

    # Return the location of the new Order
    # location_url = "unknown"
    location_url = url_for("get_order", order_id=order.id, _external=True)
    return (
        jsonify(order.serialize()),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


######################################################################
# RETRIEVE AN ORDER
######################################################################
@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    """
    Retrieve a single order

    This endpoint will return an order based on its id
    """
    app.logger.info("Request for order with id: %s", order_id)

    # See if the order exists and abort if it doesn't
    order = Order.find(order_id)
    if not order:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"order with id '{order_id}' could not be found.",
        )

    return jsonify(order.serialize()), status.HTTP_200_OK


######################################################################
# UPDATE AN EXISTING ORDER
######################################################################
@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_orders(order_id):
    """
    Update an Order

    This endpoint will update an Order based the body that is posted
    """
    app.logger.info("Request to Update an order with id [%s]", order_id)
    check_content_type("application/json")

    # Attempt to find the Order and abort if not found
    order = Order.find(order_id)
    if not order:
        abort(status.HTTP_404_NOT_FOUND, f"Order with id '{order_id}' was not found.")

    # Update the Order with the new data
    data = request.get_json()
    app.logger.info("Processing: %s", data)
    order.deserialize(data)

    # Save the updates to the database
    order.update()

    app.logger.info("Order with ID: %d updated.", order.id)
    return jsonify(order.serialize()), status.HTTP_200_OK


######################################################################
# DELETE AN ORDER
######################################################################
@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_orders(order_id):
    """
    Delete an Order

    This endpoint will delete an Order based the id specified in the path
    """
    app.logger.info("Request to Delete an order with id [%s]", order_id)

    # Delete the Order if it exists
    order = Order.find(order_id)
    if order:
        app.logger.info("Order with ID: %d found.", order.id)
        order.delete()

    app.logger.info("Order with ID: %d delete complete.", order_id)
    return {}, status.HTTP_204_NO_CONTENT


# ---------------------------------------------------------------------
#                ITEM   M E T H O D S
# ---------------------------------------------------------------------


######################################################################
# CREATE A NEW ITEM
######################################################################
@app.route("/orders/<int:order_id>/items", methods=["POST"])
def create_items(order_id):
    """
    Create an Item
    This endpoint will create an Item based on the data in the body that is posted
    """
    app.logger.info("Request to Create an Item for Order ID: %d", order_id)
    check_content_type("application/json")

    order = Order.find(order_id)
    if not order:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Order with id '{order_id}' could not be found.",
        )

    # Get the order by order id
    item = Item()
    # Get the data from the request and deserialize it
    data = request.get_json()
    item.deserialize(data)
    item.create()

    # Return the location of the new Item
    location_url = url_for(
        "get_item", order_id=order_id, product_id=item.product_id, _external=True
    )
    return (
        jsonify(item.serialize()),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


######################################################################
# LIST ITEMS
######################################################################
@app.route("/orders/<int:order_id>/items", methods=["GET"])
def list_items(order_id):
    """Returns all of the Items for an Order"""
    app.logger.info("Request for all Items for Order with id: %s", order_id)

    # See if the order exists and abort if it doesn't
    # order = Order.find(order_id)
    # if not order:
    #     abort(
    #         status.HTTP_404_NOT_FOUND,
    #         f"Order with id '{order_id}' could not be found.",
    #     )

    items = Item.find_by_order_id(order_id)
    # parse any arguments from the query string
    price = request.args.get("price")
    quantity = request.args.get("quantity")

    if price:
        app.logger.info("Find by price: %s", price)
        price = float(price)
        items = Item.find_by_price(order_id, price)
    elif quantity:
        app.logger.info("Find by quantity: %s", quantity)
        quantity = int(quantity)
        items = Item.find_by_quantity(order_id, quantity)

    # Get the items for the order
    results = [item.serialize() for item in items]
    app.logger.info("Returning %d items", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
# RETRIEVE AN ITEM FROM ORDER
######################################################################
@app.route("/orders/<int:order_id>/items/<int:product_id>", methods=["GET"])
def get_item(order_id, product_id):
    """
    Get an Item

    This endpoint returns just an item
    """
    app.logger.info(
        "Request to retrieve Item %s for Order id: %s", (product_id, order_id)
    )

    # See if the item exists and abort if it doesn't
    item = Item.find_by_product_id(order_id, product_id)
    if not item:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"product with id '{product_id}' could not be found in order '{order_id}'.",
        )

    return jsonify(item.serialize()), status.HTTP_200_OK


######################################################################
# GET ALL ORDERS
######################################################################
@app.route("/orders", methods=["GET"])
def list_orders():
    """
    Retrieve all orders
    """
    app.logger.info("Request to Retrieve All Orders")
    orders = []

    # Process the query string for order if any
    date = request.args.get("date")
    status_obj = request.args.get("status")
    address = request.args.get("address")
    customer_id = request.args.get("customer_id")

    if date:
        app.logger.info("Find by date: %s", date)
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        orders = Order.find_by_date(date_obj)
    elif status_obj:
        status_obj = int(status_obj)
        orders = Order.find_by_status(status_obj)
    elif address:
        orders = Order.find_by_address(address)
    elif customer_id:
        customer_id = int(customer_id)
        orders = Order.find_by_customer_id(customer_id)
    else:
        orders = Order.all()

    orders = sorted(
        orders,
        key=lambda order: order.date,
        reverse=True,
    )
    orders_data = [order.serialize() for order in orders]
    return jsonify(orders_data), status.HTTP_200_OK


######################################################################
# UPDATE AN ITEM
######################################################################


@app.route("/orders/<int:order_id>/items/<int:product_id>", methods=["PUT"])
def update_items(order_id, product_id):
    """
    Update an Item
    This endpoint will update an Item based the body that is posted
    """
    app.logger.info("Request to update Item %s for Item id: %s", (product_id, order_id))
    check_content_type("application/json")

    # See if the item exists and abort if it doesn't
    item = Item.find_by_product_id(order_id, product_id)
    if not item:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Item with id '{product_id}' could not be found.",
        )

    # Update from the json in the body of the request
    item.deserialize(request.get_json())
    item.order_id = order_id
    item.id = product_id
    item.update()
    return jsonify(item.serialize()), status.HTTP_200_OK


######################################################################
# DELETE AN ITEM FROM ORDER
######################################################################
@app.route("/orders/<int:order_id>/items/<int:product_id>", methods=["DELETE"])
def delete_items(order_id, product_id):
    """
    Delete an Item

    This endpoint will delete an Item based the id specified in the path
    """
    app.logger.info("Request to Delete an item with id [%s]", (product_id, order_id))

    # See if the item exists and delete it if it does
    item = Item.find_by_product_id(order_id, product_id)
    if item:
        item.delete()

    return "", status.HTTP_204_NO_CONTENT


# ---------------------------------------------------------------------
#                A C T I O N S
# ---------------------------------------------------------------------
######################################################################
# CANCEL AN ORDER
######################################################################
@app.route("/orders/<int:order_id>/cancel", methods=["PUT"])
def cancel_orders(order_id):
    """Cancel an order and change its state to 0"""
    app.logger.info("Request to cancel order with id: %d", order_id)

    # Attempt to find the Order and abort if not found
    order = Order.find(order_id)
    if not order:
        abort(status.HTTP_404_NOT_FOUND, f"Order with id '{order_id}' was not found.")

    # you can only cancel orders that are available
    if order.status == 0:
        abort(
            status.HTTP_409_CONFLICT,
            f"Order with id '{order_id}' is not available.",
        )

    # At this point you would execute code to cancel the order
    # For the moment, we will just set the status to 0
    order.status = 0
    order.update()

    app.logger.info("Order with ID: %d has been cancelled.", order_id)
    return order.serialize(), status.HTTP_200_OK


######################################################################
# DELIVERED AN ORDER
######################################################################
@app.route("/orders/<int:order_id>/deliver", methods=["PUT"])
def deliver_orders(order_id):
    """deliver an order and change its state to 3"""
    app.logger.info("Confirm delivered order with id: %d", order_id)

    # Attempt to find the Order and abort if not found
    order = Order.find(order_id)
    if not order:
        abort(status.HTTP_404_NOT_FOUND, f"Order with id '{order_id}' was not found.")

    # you can only deliver orders that are available
    if order.status == 0:
        abort(
            status.HTTP_409_CONFLICT,
            f"Order with id '{order_id}' is not available.",
        )

    # At this point you would execute code to confirm the delivery of order
    # For the moment, we will just set the status to 3
    order.status = 3
    order.update()

    app.logger.info("Order with ID: %d has been delivered.", order_id)
    return order.serialize(), status.HTTP_200_OK


######################################################################
# Checks the ContentType of a request
######################################################################
def check_content_type(content_type) -> None:
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )
