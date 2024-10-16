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

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import Order
from service.models import Item
from service.common import status  # HTTP Status Codes


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

# Todo: Place your REST API code here ...


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
    location_url = url_for("get_orders", order_id=order.id, _external=True)
    return (
        jsonify(order.serialize()),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


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
# READ AN ORDER
######################################################################
@app.route("/orders/<int:order_id>", methods=["GET"])
def get_orders(order_id):
    """
    Retrieve a single Order

    This endpoint will return an Order based on it's id
    """
    app.logger.info("Request to Retrieve an order with id [%s]", order_id)

    # Attempt to find the Order and abort if not found
    order = Order.find(order_id)
    if not order:
        abort(status.HTTP_404_NOT_FOUND, f"Order with id '{order_id}' was not found.")

    # app.logger.info("Returning order: %s", order.name)
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

    item = Item()
    # Get the data from the request and deserialize it
    data = request.get_json()
    app.logger.info("Processing: %s", data)
    item.deserialize(data)

    # Assign the order_id to the item
    item.order_id = order_id

    # Save the new Item to the database
    try:
        item.create()
    except Exception as e:
        app.logger.error("Error saving item to the database: %s", str(e))
        return (
            jsonify({"error": "Database error"}),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    app.logger.info(
        "Item with new id [%s] saved for Order ID [%s]!", item.product_id, order_id
    )

    # Return the location of the new Item
    location_url = url_for("create_items", order_id=order_id, _external=True)
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
    order = Order.find(order_id)
    if not order:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Order with id '{order_id}' could not be found.",
        )

    # Get the items for the order
    results = [item.serialize() for item in Item.find_by_order_id(order_id)]

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
    Retrieve all orders sorted by date in descending order
    """
    app.logger.info("Request to Retrieve All Orders")
    try:
        orders = Order.query.order_by(Order.date.desc()).all()
        orders_data = [order.serialize() for order in orders]
        return jsonify(orders_data), status.HTTP_200_OK
    except Exception as e:
        app.logger.error("Failed to retrieve orders: %s", str(e))
        return (
            jsonify({"error": "Failed to retrieve orders"}),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


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
