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
    Create a Order
    This endpoint will create a Order based the data in the body that is posted
    """
    app.logger.info("Request to Create a Order...")
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
    location_url = "unknown"
    #location_url = url_for("get_orders", order_id=order.id, _external=True)
    return jsonify(order.serialize()), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# UPDATE AN EXISTING ORDER
######################################################################
@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_orders(order_id):
    """
    Update an Order

    This endpoint will update an Order based the body that is posted
    """
    app.logger.info("Request to Update a order with id [%s]", order_id)
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
# CREATE A NEW ITEM
######################################################################
@app.route("/items", methods=["POST"])
def create_items():
    """
    Create an Item
    This endpoint will create an Item based the data in the body that is posted
    """
    app.logger.info("Request to Create an Item...")
    check_content_type("application/json")

    item = Item()
    # Get the data from the request and deserialize it
    data = request.get_json()
    app.logger.info("Processing: %s", data)
    try:
        item.deserialize(data)
    except Exception as e:
        app.logger.error("Error deserializing item: %s", str(e))
        return jsonify({"error": "Invalid data format"}), status.HTTP_400_BAD_REQUEST


    # Save the new Item to the database
    try:
        item.create()
    except Exception as e:
        app.logger.error("Error saving item to the database: %s", str(e))
        return jsonify({"error": "Database error"}), status.HTTP_500_INTERNAL_SERVER_ERROR

    app.logger.info("Item with new id [%s] saved!", item.product_id)

    # Todo : uncomment this code when get_order is implemented


    # Return the location of the new Item
    location_url = "unknown"
    #location_url = url_for("get_orders", order_id=order.id, _external=True)
    return jsonify(item.serialize()), status.HTTP_201_CREATED, {"Location": location_url}



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