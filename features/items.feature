Feature: The Order service back-end
    As an Order site Admin
    I need a RESTful catalog service
    So that I can keep track of all my orders

Background:
    Given the following items:
        |product_id   | order_id    | price          | quantity   | 
        |1            | 2           | 2.0            | 1          | 
        |2            | 3           | 1.0	         | 2          | 

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Order Demo RESTful Service" in the title
    And I should not see "404 Not Found"


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
