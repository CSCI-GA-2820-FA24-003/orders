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
    status = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Numeric, nullable=False)
    address = db.Column(db.String(64), nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Order {self.id} id=[{self.id}]>"

    def serialize(self):
        """Converts an Order into a dictionary"""
        order = {
            "id": self.id,
            "date": self.date_joined.isoformat(),
            "status": self.status,
            "amount": self.amount,
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
            self.id = data["id"]
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

    # @classmethod
    # def find_by_name(cls, name):
    #     """Returns all Accounts with the given name

    #     Args:
    #         name (string): the name of the Accounts you want to match
    #     """
    #     logger.info("Processing name query for %s ...", name)
    #     return cls.query.filter(cls.name == name)
