Feature: The Item service back-end
    As an Order site Admin
    I need a RESTful catalog service
    So that I can keep track of all items of my orders

Background:
    Given the following order
        | amount | address           | status   | date         | customer_id |
        | 0.0    | item address      | 1        | 2024-12-01   | 100         |
    Given the following Items
        |product_id   | price          | quantity   | 
        |123          | 10.0           | 7          | 
        |456          | 20.0	       | 8          | 

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Order Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create an Item
    When I visit the "Home Page"
    And I press the "Order Clear" button
    And I press the "Order Search" button
    Then I should see "item address" in the "Address" field
    When I copy the "ID" field
    When I paste the Item "Order ID" field
    And I set the Item "Product ID" to "789"
    And I set the Item "Price" to "10"
    And I set the Item "Quantity" to "1"
    When I press the "Item Create" button
    Then I should see the message "Success"
    When I press the "Item Clear" button
    When I copy the "ID" field
    And I paste the Item "Order ID" field
    And I press the "Item Search" button
    Then I should see the message "Success"
    And I should see "789" in the item results
    And I should see "10" in the item results

Scenario: List all Items of an Order
    When I visit the "Home Page"
    And I press the "Order Clear" button
    And I press the "Order Search" button
    Then I should see "item address" in the "Address" field
    When I copy the "ID" field
    When I paste the Item "Order ID" field
    And I press the "Item Search" button
    Then I should see the message "Success"
    And I should see "123" in the Item results
    And I should see "456" in the Item results

Scenario: Search Item by Price
    When I visit the "Home Page"
    And I press the "Order Clear" button
    And I press the "Order Search" button
    Then I should see "item address" in the "Address" field
    When I copy the "ID" field
    When I paste the Item "Order ID" field
    When I set the Item "Price" to "10"
    And I press the "Item Search" button
    Then I should see the message "Success"
    And I should see "123" in the Item results
    And I should see "7" in the Item results
    And I should not see "456" in the Item results

Scenario: Search Item by Quantity
    When I visit the "Home Page"
    And I press the "Order Clear" button
    And I press the "Order Search" button
    Then I should see "item address" in the "Address" field
    When I copy the "ID" field
    When I paste the Item "Order ID" field
    When I set the Item "Quantity" to "7"
    And I press the "Item Search" button
    Then I should see the message "Success"
    And I should see "123" in the Item results
    And I should see "10" in the Item results
    And I should not see "456" in the Item results

Scenario: Read an Item
    When I visit the "Home Page"
    And I press the "Order Clear" button
    And I press the "Order Search" button
    Then I should see "item address" in the "Address" field
    When I copy the "ID" field
    When I paste the Item "Order ID" field
    When I set the Item "Product ID" to "123"
    And I press the "Item Retrieve" button
    Then I should see the message "Success"
    And I should see "10" in the Item "Price" field
    And I should see "7" in the Item "Quantity" field

Scenario: Update an Item
    When I visit the "Home Page"
    And I press the "Order Clear" button
    And I press the "Order Search" button
    Then I should see "item address" in the "Address" field
    When I copy the "ID" field
    When I paste the Item "Order ID" field
    When I set the Item "Product ID" to "123"
    And I press the "Item Retrieve" button
    Then I should see the message "Success"
    And I should see "10" in the Item "Price" field
    And I should see "7" in the Item "Quantity" field
    When I change Item "Quantity" to "11"
    And I press the "Item Update" button
    Then I should see the message "Success"
    When I press the "Item Clear" button
    Then the Item "Price" field should be empty
    Then the Item "Quantity" field should be empty
    When I copy the "ID" field
    When I paste the Item "Order ID" field
    When I set the Item "Product ID" to "123"
    And I press the "Item Retrieve" button
    Then I should see the message "Success"
    And I should see "10" in the Item "Price" field
    And I should see "11" in the Item "Quantity" field

Scenario: Delete an Item
    When I visit the "Home Page"
    And I press the "Order Clear" button
    And I press the "Order Search" button
    Then I should see "item address" in the "Address" field
    When I copy the "ID" field
    When I paste the Item "Order ID" field
    When I set the Item "Product ID" to "123"
    And I press the "Item Retrieve" button
    Then I should see the message "Success"
    And I should see "10" in the Item "Price" field
    And I should see "7" in the Item "Quantity" field
    When I press the "Item Delete" button
    Then I should see the message "Item has been Deleted!"
    And the Item "Order ID" field should be empty
    And the Item "Product ID" field should be empty
    And the Item "Price" field should be empty
    And the Item "Quantity" field should be empty
    When I paste the Item "Order ID" field
    When I set the Item "Product ID" to "123"
    And I press the "Item Retrieve" button
    Then I should see the message "could not be found"