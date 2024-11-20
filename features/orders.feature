Feature: The Order service back-end
    As an Order site Admin
    I need a RESTful catalog service
    So that I can keep track of all my orders

Background:
    Given the following orders
        | amount | address           | status | date       | customer_id |
        | 0.0    | fake address 1    | 0      | 2019-11-18 | 1           |
        | 10.0   | fake address 2    | 1      | 2020-08-13 | 2           |
        | 20.0   | fake address 3    | 2      | 2021-04-01 | 3           |
        | 30.0   | fake address 4    | 3      | 2018-06-04 | 4           |
    Given the following items:
        |product_id   | order_id    | price          | quantity   | 
        |1            | 2           | 2.0            | 1          | 
        |2            | 3           | 1.0	         | 2          | 

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Order Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create an Order
    When I visit the "Home Page"
    And I set the "Amount" to "0"
    And I select "Preparing" in the "Status" dropdown
    And I set the "Address" to "Fake Address"
    And I set the "Customer ID" to "1"
    And I set the "Date" to "06-16-2022"
    And I press the "Order Create" button
    Then I should see the message "Success"
    When I copy the "ID" field
    And I press the "Order Clear" button
    Then the "ID" field should be empty
    And the "Amount" field should be empty
    And the "Address" field should be empty
    And the "Customer ID" field should be empty
    When I paste the "ID" field
    And I press the "Order Retrieve" button
    Then I should see the message "Success"
    And I should see "0" in the "Amount" field
    And I should see "Preparing" in the "Status" dropdown
    And I should see "Fake Address" in the "Address" field
    And I should see "1" in the "Customer ID" field
    And I should see "2022-06-16" in the "Date" field

Scenario: Read an Order
    When I visit the "Home Page"
    And I press the "Order Clear" button
    And I set the "address" to "fake address 1"
    And I press the "Order Search" button
    Then I should see the message "Success"
    When I copy the "ID" field
    And I press the "Order Clear" button
    Then the "ID" field should be empty
    And the "Amount" field should be empty
    And the "Address" field should be empty
    And the "Customer ID" field should be empty
    When I paste the "ID" field
    And I press the "Order Retrieve" button
    Then I should see the message "Success"
    And I should see "0" in the "Amount" field
    And I should see "fake address 1" in the "Address" field
    And I should see "Cancelled" in the "Status" dropdown
    And I should see "2019-11-18" in the "Date" field
    And I should see "1" in the "Customer ID" field

Scenario: Update an Order
    When I visit the "Home Page"
    And I press the "Order Clear" button
    And I set the "Address" to "fake address 1"
    And I press the "Order Search" button
    Then I should see the message "Success"
    And I should see "0" in the "Amount" field
    And I should see "fake address 1" in the "Address" field
    And I should see "Cancelled" in the "Status" dropdown
    And I should see "2019-11-18" in the "Date" field
    And I should see "1" in the "Customer ID" field
    When I change "Address" to "fake address changed"
    And I press the "Order Update" button
    Then I should see the message "Success"
    When I copy the "ID" field
    And I press the "Order Clear" button
    And I paste the "ID" field
    And I press the "Order Retrieve" button
    Then I should see the message "Success"
    And I should see "fake address changed" in the "Address" field
    When I press the "Order Clear" button
    And I press the "Order Search" button
    Then I should see the message "Success"
    And I should see "fake address changed" in the order results
    And I should not see "fake address 1" in the order results

Scenario: Delete an Order
    When I visit the "Home Page"
    And I press the "Order Clear" button
    And I set the "address" to "fake address 1"
    And I press the "Order Search" button
    Then I should see the message "Success"
    And I should see "0" in the "Amount" field
    And I should see "fake address 1" in the "Address" field
    And I should see "Cancelled" in the "Status" dropdown
    And I should see "2019-11-18" in the "Date" field
    And I should see "1" in the "Customer ID" field
    When I copy the "ID" field
    And I press the "Order Delete" button
    Then I should see the message "Order has been Deleted!"
    And the "ID" field should be empty
    And the "Amount" field should be empty
    And the "Address" field should be empty
    And the "Customer ID" field should be empty
    When I paste the "ID" field
    And I press the "Order Retrieve" button
    Then I should see the message "404 Not Found"

Scenario: List all Orders
    When I visit the "Home Page"
    And I press the "Order Clear" button
    And I press the "Order Search" button
    Then I should see the message "Success"
    And I should see "fake address 1" in the order results
    And I should see "fake address 2" in the order results
    And I should see "fake address 3" in the order results
    And I should see "fake address 4" in the order results
    And I should not see "fake address 5" in the order results

Scenario: Search by Status
    When I visit the "Home Page"
    And I press the "Order Clear" button
    And I select "Preparing" in the "Status" dropdown
    And I press the "Order Search" button
    Then I should see the message "Success"
    And I should see "fake address 2" in the order results
    And I should not see "fake address 1" in the order results

Scenario: Search by address
    When I visit the "Home Page"
    And I press the "Order Clear" button
    And I set the "Address" to "fake address 1"
    And I press the "Order Search" button
    Then I should see the message "Success"
    And I should see "Cancelled" in the order results
    And I should not see "Preparing" in the order results

Scenario: Search by Customer ID
    When I visit the "Home Page"
    And I press the "Order Clear" button
    And I set the "Customer ID" to "1"
    And I press the "Order Search" button
    Then I should see the message "Success"
    And I should see "Cancelled" in the order results
    And I should not see "Preparing" in the order results

Scenario: Search by Date
    When I visit the "Home Page"
    And I press the "Order Clear" button
    And I set the "Date" to "11-18-2019"
    And I press the "Order Search" button
    Then I should see the message "Success"
    And I should see "fake address 1" in the order results
    And I should not see "fake address 2" in the order results

Scenario: Cancel an Order
    When I visit the "Home Page"
    And I press the "Order Search" button
    Then I should see "fake address 2" in the "Address" field
    And I should see "Preparing" in the "Status" dropdown
    When I press the "Order Cancel" button
    Then I should see the message "Order has been Cancelled!"
    And I should see "fake address 2" in the "Address" field
    And I should see "Cancelled" in the "Status" dropdown

Scenario: Create an Item
    When I visit the "Home Page"
    And I set the "Item Order ID" to "{order_id}"
    And I set the "Product ID" to "100"
    And I set the "Quantity" to "10"
    And I set the "Price" to "9.99"
    And I press the "Create Item" button
    Then I should see the message "Success"
    When I copy the "Item ID" field
    And I press the "Retrieve Item" button
    Then I should see the message "Success"
    And I should see "100" in the "Product ID" field
    And I should see "10" in the "Quantity" field
    And I should see "9.99" in the "Unit Price" field


Scenario: List Items
    When I visit the "Home Page"
    And I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    When I press the "Clear Item" button
    Then the "Item ID" field should be empty
    When I copy the "Order ID" field
    And I press the "Clear" button
    And I paste the "Item Order ID" field
    And I press the "Search Item" button
    Then I should see the message "Success"
    And I should see "product 1" in the "Item" results
    And I should see "product 2" in the "Item" results


Scenario: Query Items
    When I visit the "Home Page"
    And I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    Then I save the "Order Id" field as "order_id"
    When I set the "Item Order ID" to "{order_id}"
    And I set the "Product ID" to "2"
    And I press the "Search Item" button
    Then I should see the message "Success"
    And I should see "Product 2" in the "Item" results
    And I should not see "Product 1" in the "Item" results
    When I press the "Clear Item" button
    Then the "Product ID" field should be empty
    When I set the "Item Order ID" to "{order_id}"
    And I press the "Search Item" button
    Then I should see the message "Success"
    And I should see "Product" in the "Name" field


Scenario: Read an Item
    When I visit the "Home Page"
    And I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Order Id" field
    And I paste the "Item Order ID" field
    And I press the "Search Item" button
    Then I should see the message "Success"
    When I copy the "Item Id" field
    And I press the "Clear Item" button
    And I paste the "Item Id" field
    When I copy the "Order Id" field
    And I paste the "Item Order ID" field
    And I press the "Retrieve Item" button
    Then I should see the message "Success"
    And I should see "1" in the "Product ID" field
    And I should see "1" in the "Quantity" field
    And I should see "2.0" in the "Price" field



Scenario: Update an Item
    When I visit the "Home Page"
    And I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Order Id" field
    And I paste the "Item Order ID" field
    And I press the "Search Item" button
    Then I should see the message "Success"
    When I copy the "Item Id" field
    And I press the "Clear Item" button
    And I paste the "Item Id" field
    When I copy the "Order Id" field
    And I paste the "Item Order ID" field
    And I press the "Retrieve Item" button
    Then I should see the message "Success"
    When I set the "Quantity" to "3"
    And I press the "Update Item" button
    Then I should see the message "Success"
    When I copy the "Item Id" field
    And I press the "Clear Item" button
    And I paste the "Item Id" field
    When I copy the "Order Id" field
    And I paste the "Item Order ID" field
    And I press the "Retrieve Item" button
    Then I should see the message "Success"
    And I should see "3" in the "Quantity" field

Scenario: Delete an Item
    When I visit the "Home Page"
    And I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Order Id" field
    And I paste the "Item Order ID" field
    And I press the "Search Item" button
    Then I should see the message "Success"
    When I copy the "Item Id" field
    And I press the "Clear Item" button
    And I paste the "Item Id" field
    When I copy the "Order Id" field
    And I paste the "Item Order ID" field
    And I press the "Retrieve Item" button
    Then I should see the message "Success"
    And I should see "1" in the "Product ID" field
    And I should see "1" in the "Quantity" field
    And I should see "2.0" in the "Unit Price" field
    When I press the "Delete Item" button
    Then I should see the message "Item has been Deleted!"
