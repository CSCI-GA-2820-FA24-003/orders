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
# cspell: ignore= userid, backref
"""
Persistent Base class for database CRUD functions
"""

import logging
from .persistent_base import db, PersistentBase, DataValidationError

logger = logging.getLogger("flask.app")


######################################################################
#  O R D E R   M O D E L
######################################################################
class Item(db.Model, PersistentBase):
    """
    Class that represents an Item
    """

    # Table Schema
    product_id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_id = db.Column(
        db.Integer,
        db.ForeignKey("order.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    price = db.Column(db.Numeric, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order = db.relationship("Order", backref="item", passive_deletes=True)

    def amount(self):
        return self.price * self.quantity

    def __repr__(self):
        return f"<Order {self.order_id} Product id=[{self.product_id}]>"

    def serialize(self):
        """Converts an Order into a dictionary"""
        item = {
            "order_id": self.order_id,
            "product_id": self.product_id,
            "price": self.price,
            "quantity": self.quantity,
        }

        return item

    def deserialize(self, data):
        """
        Populates an Order from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.order_id = data["order_id"]
            self.product_id = data["product_id"]
            self.price = data["price"]
            self.quantity = data["quantity"]
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid Item: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Item: body of request contained bad or no data " + str(error)
            ) from error

        return self

    @classmethod
    def find_by_order_id(cls, order_id):
        """Returns all Items with the given order id

        Args:
            order_id (Integer): the id of the order you want to match
        """
        logger.info("Processing order_id query for %s ...", order_id)
        return cls.query.filter(cls.order_id == order_id).all()

    @classmethod
    def find_by_product_id(cls, order_id, product_id):
        """Returns items with the given order_id and product_id

        Args:
            order_id (Integer): the id of the order you want to match
            product_id (Integer): the id of the product you want to match
        """
        logger.info(
            "Processing order_id, product_id query for %s %s ...", order_id, product_id
        )
        return cls.query.filter(
            cls.order_id == order_id, cls.product_id == product_id
        ).first()
