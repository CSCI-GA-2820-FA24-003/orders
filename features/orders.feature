Feature: The Order service back-end
    As an Order site Admin
    I need a RESTful catalog service
    So that I can keep track of all my orders

Background:
    Given the following orders
        | id       | amount | address           | status  | date       | customer_id |
        | 1        | 0.0    | fake address 1    | 0       | 2019-11-18 | 1           |
        | 2        | 10.0   | fake address 2    | 1       | 2020-08-13 | 2           |
        | 3        | 20.0   | fake address 3    | 2       | 2021-04-01 | 3           |
        | 4        | 30.0   | fake address 4    | 3       | 2018-06-04 | 4           |

    Given the following items:
        |product_id   | order_id    | price          | quantity   | 
        |1            | 2           | 2.0            | 1          | 
        |2            | 3           | 1.0	         | 2          | 


Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Order Demo RESTful Service" in the title
    And I should not see "404 Not Found"