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
from datetime import date
from .persistent_base import db, PersistentBase, DataValidationError

logger = logging.getLogger("flask.app")


######################################################################
#  O R D E R   M O D E L
######################################################################
class Order(db.Model, PersistentBase):
    """
    Class that represents an Order
    """

    # Table Schema
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date = db.Column(db.Date(), nullable=False, default=date.today())
    status = db.Column(
        db.Integer, nullable=False
    )  # 1: preparing, 2: delivering, 3: delivered, 0: cancelled
    amount = db.Column(db.Numeric, nullable=False)
    address = db.Column(db.String(64), nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Order {self.id} id=[{self.id}]>"

    def serialize(self):
        """Converts an Order into a dictionary"""
        order = {
            "id": self.id,
            # Changed from "date": self.date_joined.isoformat(),
            "date": self.date.isoformat(),
            "status": self.status,
            # Changed from "amount": self.amount,
            "amount": float(self.amount),
            "address": self.address,
            "customer_id": self.customer_id,
        }

        return order

    def deserialize(self, data):
        """
        Populates an Order from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.date = date.fromisoformat(data["date"])
            self.status = data["status"]
            self.amount = data["amount"]
            self.address = data["address"]
            self.customer_id = data["customer_id"]
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid Order: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Order: body of request contained bad or no data " + str(error)
            ) from error

        return self

    @classmethod
    def update_amount(cls, order_id, amount):
        """update the amount in an order

        Args:
            order_id: the id of the order you want to match
        """
        logger.info("Processing order update for %s ...", order_id)
        return cls.query.filter(cls.id == order_id).update({cls.amount: amount})

    ######################################################################
    #  Q U E R Y    F U N C T I O N S
    ######################################################################
    @classmethod
    def find_by_date(cls, date_obj):
        """Returns all orders with the given date

        Args:
            date (date object): the date of the orders you want to match
        """
        logger.info("Processing date query for %s ...", date_obj)
        return cls.query.filter(cls.date == date_obj).all()

    @classmethod
    def find_by_address(cls, address):
        """Returns all orders with the given address

        Args:
            address (string): the address of the orders you want to match
        """
        logger.info("Processing address query for %s ...", address)
        return cls.query.filter(cls.address == address).all()

    @classmethod
    def find_by_customer_id(cls, customer_id):
        """Returns all orders with the given customer_id

        Args:
            customer_id (int): the customer_id of the orders you want to match
        """
        logger.info("Processing customer_id query for %s ...", customer_id)
        return cls.query.filter(cls.customer_id == customer_id).all()

    @classmethod
    def find_by_status(cls, customer_id, status):
        """Returns all orders with the given customer_id and status

        Args:
            customer_id (int): the customer_id of the orders you want to match
            status (int): the status of the orders you want to match
        """
        logger.info("Processing customer_id and status query for %s ...", customer_id)
        return cls.query.filter(
            cls.customer_id == customer_id, cls.status == status
        ).all()

    @classmethod
    def find_by_amount(cls, amount):
        """Returns all orders with the given amount

        Args:
            amount (Numeric): the amount of the orders you want to match
        """
        logger.info("Processing amount query for %s ...", amount)
        return cls.query.filter(cls.amount == amount).all()

    # @classmethod
    # def find_by_name(cls, name):
    #     """Returns all Accounts with the given name

    #     Args:
    #         name (string): the name of the Accounts you want to match
    #     """
    #     logger.info("Processing name query for %s ...", name)
    #     return cls.query.filter(cls.name == name)
