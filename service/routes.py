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
Order Service with Swagger

Paths:
------ Order ------
GET / - Displays a UI for Selenium testing
GET /orders - Returns a list all of the Orders
GET /orders/{order_id} - Returns the Order with a given id number
POST /orders - creates a new Order record in the database
PUT /orders/{order_id} - updates a Order record in the database
DELETE /orders/{id} - deletes an Order record in the database
PUT /orders/{order_id}/cancel - cancel an Order
------ Item ------
GET /orders/{order_id}/items - Returns a list all of the items of an order
GET /orders/{order_id}/items/{product_id} - Returns the item with the given order id and product id
POST /orders/{order_id}/items - creates a new Item record in the database
PUT /orders/{order_id}/items/{product_id} - updates an Item record in the database
DELETE /orders/{order_id}/items/{product_id} - deletes an Order record in the database
"""

from datetime import datetime
from flask import jsonify, request
from flask import current_app as app  # Import Flask application
from flask_restx import Api, Resource, fields, reqparse
from service.models import Order
from service.models import Item
from service.common import status  # HTTP Status Codes

######################################################################
# Configure Swagger before initializing it
######################################################################
api = Api(
    app,
    version="1.0.0",
    title="Order Demo REST API Service",
    description="This is an Order server.",
    default="orders",
    default_label="Order operations",
    doc="/apidocs",  # default also could use doc='/apidocs/'
    prefix="/api",
)


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


# Define the model so that the docs reflect what can be sent
create_model = api.model(
    "Order",
    {
        "date": fields.Date(required=True, description="The date of the order"),
        "status": fields.Integer(
            required=True,
            description="The status of the order, (0: Cancelled, 1: Preparing, 2: Delivering, 3: Delivered)",
        ),
        "amount": fields.Float(description="The total amount of the order"),
        "address": fields.String(required=True, description="The address of the order"),
        "customer_id": fields.Integer(
            required=True, description="The id of the customer of this order"
        ),
    },
)

order_model = api.inherit(
    "OrderModel",
    create_model,
    {
        "id": fields.Integer(
            readOnly=True, description="The unique id assigned internally by service"
        ),
    },
)

# query string arguments
order_args = reqparse.RequestParser()
order_args.add_argument(
    "status", type=int, location="args", required=False, help="List Orders by status"
)
order_args.add_argument(
    "address", type=str, location="args", required=False, help="List Orders by address"
)
order_args.add_argument(
    "customer_id",
    type=int,
    location="args",
    required=False,
    help="List Orders by customer id",
)
order_args.add_argument(
    "date",
    type=str,
    location="args",
    required=False,
    help="List Orders by date",
)


######################################################################
#  PATH: /orders/{order_id}
######################################################################
@api.route("/orders/<int:order_id>")
@api.param("order_id", "The Order identifier")
class OrderResource(Resource):
    """
    OrderResource class

    Allows the manipulation of a single Order
    GET /order{order_id} - Returns an Order with the order_id
    PUT /order{order_id} - Update an Order with the order_id
    DELETE /order{order_id} -  Deletes an Order with the order_id
    """

    # ------------------------------------------------------------------
    # RETRIEVE AN ORDER
    # ------------------------------------------------------------------
    @api.doc("get_orders")
    @api.response(404, "Order not found")
    @api.marshal_with(order_model)
    def get(self, order_id):
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

        return order.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING ORDER
    # ------------------------------------------------------------------
    @api.doc("update_orders")
    @api.response(404, "Order not found")
    @api.response(400, "The posted Order data was not valid")
    @api.expect(order_model)
    @api.marshal_with(order_model)
    def put(self, order_id):
        """
        Update an Order

        This endpoint will update an Order based the body that is posted
        """
        app.logger.info("Request to Update an order with id [%s]", order_id)
        check_content_type("application/json")
        # Attempt to find the Order and abort if not found
        order = Order.find(order_id)
        if not order:
            abort(
                status.HTTP_404_NOT_FOUND, f"Order with id '{order_id}' was not found."
            )
        app.logger.debug("Payload = %s", api.payload)
        data = api.payload
        order.deserialize(data)
        order.id = order_id
        order.update()
        app.logger.info("Order with ID: %d updated.", order.id)
        return order.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE AN ORDER
    # ------------------------------------------------------------------
    @api.doc("delete_orders")
    @api.response(204, "Order deleted")
    def delete(self, order_id):
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
        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /orders
######################################################################
@api.route("/orders", strict_slashes=False)
class OrderCollection(Resource):
    """Handles all interactions with collections of Orders"""

    # ------------------------------------------------------------------
    # LIST ALL ORDERS
    # ------------------------------------------------------------------
    @api.doc("list_orders")
    @api.expect(order_args, validate=True)
    @api.marshal_list_with(order_model)
    def get(self):
        """
        Retrieve all orders
        """
        app.logger.info("Request to Retrieve All Orders")
        orders = []
        args = order_args.parse_args()
        app.logger.info(f"Parsed arguments: {args}")

        if args["date"]:
            app.logger.info("Filtering by date: %s", args["date"])
            date_obj = datetime.strptime(args["date"], "%Y-%m-%d").date()
            orders = Order.find_by_date(date_obj)
        elif args["status"]:
            app.logger.info("Filtering by status: %s", args["status"])
            # status_obj = int(args["status"])
            orders = Order.find_by_status(args["status"])
        elif args["address"]:
            app.logger.info("Filtering by address: %s", args["address"])
            orders = Order.find_by_address(args["address"])
        elif args["customer_id"]:
            app.logger.info("Filtering by customer id: %s", args["customer_id"])
            # customer_id = int(args["customer_id"])
            orders = Order.find_by_customer_id(args["customer_id"])
        else:
            app.logger.info("Returning unfiltered list.")
            orders = Order.all()

        orders = sorted(
            orders,
            key=lambda order: order.date,
            reverse=True,
        )
        app.logger.info("[%s] Orders returned", len(orders))
        results = [order.serialize() for order in orders]
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW ORDER
    # ------------------------------------------------------------------
    @api.doc("create_orders")
    @api.response(400, "The posted order data was not valid")
    @api.response(415, "Content-Type must be application/json")
    @api.expect(create_model)
    @api.marshal_with(order_model, code=201)
    def post(self):
        """
        Create an Order
        This endpoint will create an Order based the data in the body that is posted
        """
        app.logger.info("Request to Create an Order...")
        check_content_type("application/json")
        order = Order()
        app.logger.debug("Payload = %s", api.payload)
        order.deserialize(api.payload)
        order.create()
        app.logger.info("Order with new id [%s] saved!", order.id)
        location_url = api.url_for(OrderResource, order_id=order.id, _external=True)
        return order.serialize(), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
#  PATH: /orders/{id}/cancel
######################################################################
@api.route("/orders/<int:order_id>/cancel")
@api.param("order_id", "The Order identifier")
class CancelResource(Resource):
    """Cancel actions on an Order"""

    @api.doc("cancel_orders")
    @api.response(404, "Order not found")
    @api.response(409, "The Order is not available for cancel")
    def put(self, order_id):
        """Cancel an order"""
        app.logger.info("Request to cancel order with id: %d", order_id)

        # Attempt to find the Order and abort if not found
        order = Order.find(order_id)
        if not order:
            abort(
                status.HTTP_404_NOT_FOUND, f"Order with id '{order_id}' was not found."
            )
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


# ---------------------------------------------------------------------
#                I T E M
# ---------------------------------------------------------------------
# Define the model so that the docs reflect what can be sent
item_model = api.model(
    "ItemModel",
    {
        "order_id": fields.Integer(
            readOnly=True, required=True, description="The order id of this item"
        ),
        "product_id": fields.Integer(
            readOnly=True, required=True, description="The product id of this item"
        ),
        "price": fields.Float(
            description="The price of the item",
        ),
        "quantity": fields.Integer(
            description="The quantity of the item",
        ),
    },
)

# query string arguments
item_args = reqparse.RequestParser()
item_args.add_argument(
    "price", type=float, location="args", required=False, help="List Items by price"
)
item_args.add_argument(
    "quantity", type=int, location="args", required=False, help="List Items by quantity"
)


######################################################################
#  PATH: /orders/{order_id}/items/{product_id}
######################################################################
@api.route("/orders/<int:order_id>/items/<int:product_id>")
@api.param("order_id", "product_id", "The Item identifier")
class ItemResource(Resource):
    """
    ItemResource class

    Allows the manipulation of a single Item
    GET /orders/{order_id}/items/{product_id} - Returns an Item with the order id and product id
    PUT /orders/{order_id}/items/{product_id} - Update an Item with the order id and product id
    DELETE /orders/{order_id}/items/{product_id} -  Deletes an Item with the order id and product id
    """

    # ------------------------------------------------------------------
    # RETRIEVE AN ITEM
    # ------------------------------------------------------------------
    @api.doc("get_items")
    @api.response(404, "Item not found")
    @api.marshal_with(item_model)
    def get(self, order_id, product_id):
        """
        Get an Item

        This endpoint will return an Item based on it's order id and product id
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

        return item.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING ITEM
    # ------------------------------------------------------------------
    @api.doc("update_items")
    @api.response(400, "The posted Item data was not valid")
    @api.response(404, "Item not found")
    @api.response(415, "Content-Type must be application/json")
    @api.expect(item_model)
    @api.marshal_with(item_model)
    def put(self, order_id, product_id):
        """
        Update an Item
        This endpoint will update an Item based the body that is posted
        """
        app.logger.info(
            "Request to update Item %s for Order: %s", (product_id, order_id)
        )
        check_content_type("application/json")
        # See if the item exists and abort if it doesn't
        item = Item.find_by_product_id(order_id, product_id)
        if not item:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Item with id '{product_id}' could not be found in order '{order_id}'",
            )
        # Update from the json in the body of the request
        app.logger.debug("Payload = %s", api.payload)
        data = api.payload
        item.deserialize(data)
        # item.order_id = order_id
        # item.product_id = product_id
        item.update()
        return item.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE AN ITEM
    # ------------------------------------------------------------------
    @api.doc("delete_items")
    @api.response(204, "Item deleted")
    def delete(self, order_id, product_id):
        """
        Delete an Item

        This endpoint will delete an Item based the id specified in the path
        """
        app.logger.info(
            "Request to Delete an item with id [%s] in order [%s]",
            (product_id, order_id),
        )

        # See if the item exists and delete it if it does
        item = Item.find_by_product_id(order_id, product_id)
        if item:
            item.delete()

        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /orders/{order_id}/items
######################################################################
@api.route("/orders/<int:order_id>/items", strict_slashes=False)
class ItemCollection(Resource):
    """Handles all interactions with collections of Items"""

    # ------------------------------------------------------------------
    # LIST ALL ITEMS OF AN ORDER
    # ------------------------------------------------------------------
    @api.doc("list_items")
    @api.response(404, "Order not found")
    @api.expect(item_args, validate=True)
    @api.marshal_list_with(item_model)
    def get(self, order_id):
        """Returns all of the Items for an Order"""
        app.logger.info("Request for all Items for Order with id: %s", order_id)

        # See if the order exists and abort if it doesn't
        order = Order.find(order_id)
        if not order:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Order with id '{order_id}' could not be found.",
            )

        items = []
        args = item_args.parse_args()

        if args["price"]:
            app.logger.info("Filtering by price: %s", args["price"])
            # price = float(args["price"])
            items = Item.find_by_price(order_id, args["price"])
        elif args["quantity"]:
            app.logger.info("Filtering by quantity: %s", args["quantity"])
            # quantity = int(args["quantity"])
            items = Item.find_by_quantity(order_id, args["quantity"])
        else:
            items = Item.find_by_order_id(order_id)
        # Get the items for the order
        app.logger.info("[%s] Items returned", len(items))
        results = [item.serialize() for item in items]
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW ITEM
    # ------------------------------------------------------------------
    @api.doc("create_items")
    @api.response(400, "The posted data was not valid")
    @api.response(404, "Order not found")
    @api.response(415, "Content-Type must be application/json")
    @api.expect(item_model)
    @api.marshal_with(item_model, code=201)
    def post(self, order_id):
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
        app.logger.debug("Payload = %s", api.payload)
        item.deserialize(api.payload)
        item.create()

        app.logger.info(
            "Item with order id [%s] and product id [%s] created!",
            item.order_id,
            item.product_id,
        )
        location_url = api.url_for(
            ItemResource,
            order_id=item.order_id,
            product_id=item.product_id,
            _external=True,
        )
        return item.serialize(), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# Checks the ContentType of a request
######################################################################
def abort(error_code: int, message: str):
    """Logs errors before aborting"""
    app.logger.error(message)
    api.abort(error_code, message)


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
