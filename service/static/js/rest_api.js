$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_order_form_data(res) {
        $("#order_id").val(res.id);
        $("#order_amount").val(res.amount);
        $("#order_status").val(res.status);
        $("#order_address").val(res.address);
        $("#order_customer_id").val(res.customer_id);
        $("#order_date").val(res.date);
    }

    /// Clears all form fields
    function clear_order_form_data() {
        $("#order_id").val("");
        $("#order_amount").val("");
        $("#order_status").val("");
        $("#order_address").val("");
        $("#order_customer_id").val("");
        $("#order_date").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create an order
    // ****************************************

    $("#order_create-btn").click(function () {
        let amount = $("#order_amount").val();
        let status = $("#order_status").val();
        let address = $("#order_address").val();
        let customer_id = $("#order_customer_id").val();
        let date = $("#order_date").val();

        let data = {
            "amount": amount,
            "status": status,
            "address": address,
            "customer_id": customer_id,
            "date": date
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/orders",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_order_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update an order
    // ****************************************

    $("#order_update-btn").click(function () {

        let order_id = $("#order_id").val();
        let amount = $("#order_amount").val();
        let status = $("#order_status").val();
        let address = $("#order_address").val();
        let customer_id = $("#order_customer_id").val();
        let date = $("#order_date").val();

        let data = {
            "id": order_id,
            "amount": amount,
            "status": status,
            "address": address,
            "customer_id": customer_id,
            "date": date
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/orders/${order_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_order_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve an order
    // ****************************************

    $("#order_retrieve-btn").click(function () {

        let order_id = $("#order_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/orders/${order_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_order_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_order_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete an order
    // ****************************************

    $("#order_delete-btn").click(function () {

        let order_id = $("#order_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/orders/${order_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_order_form_data()
            flash_message("Order has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Cancel an order
    // ****************************************

    $("#order_cancel-btn").click(function () {

        let order_id = $("#order_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/orders/${order_id}/cancel`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            update_order_form_data(res)
            flash_message("Order has been Cancelled!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#order_clear-btn").click(function () {
        $("#order_id").val("");
        $("#flash_message").empty();
        clear_order_form_data()
    });

    // ****************************************
    // Search for a order
    // ****************************************

    $("#order_search-btn").click(function () {

        let status = $("#order_status").val();
        let address = $("#order_address").val();
        let customer_id = $("#order_customer_id").val();
        let date = $("#order_date").val();

        let queryString = ""

        if (status) {
            queryString += 'status=' + status
        }else if (address) {
            queryString += 'address=' + address
        }else if (date) {
            queryString += 'date=' + date
        }else if (customer_id) {
            queryString += 'customer_id=' + customer_id
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/orders?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#order_search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Amount</th>'
            table += '<th class="col-md-2">Status</th>'
            table += '<th class="col-md-2">Address</th>'
            table += '<th class="col-md-2">Customer ID</th>'
            table += '<th class="col-md-2">Date</th>'
            table += '</tr></thead><tbody>'
            let first_order = "";
            const status_map = {0: "Cancelled", 1: "Preparing", 2: "Delivering", 3: "Delivered"};
            for(let i = 0; i < res.length; i++) {
                let order = res[i];
                
                table +=  `<tr id="row_${i}"><td>${order.id}</td><td>${order.amount}</td><td>${status_map[order.status]}</td><td>${order.address}</td><td>${order.customer_id}</td><td>${order.date}</td></tr>`;
                if (i == 0) {
                    first_order = order;
                }
            }
            table += '</tbody></table>';
            $("#order_search_results").append(table);

            // copy the first result to the form
            if (first_order != "") {
                update_order_form_data(first_order)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });


    // ****************************************
    //  I T E M    U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_item_form_data(res) {
        $("#item_order_id").val(res.order_id);
        $("#item_product_id").val(res.product_id);
        $("#item_price").val(res.price);
        $("#item_quantity").val(res.quantity);
    }

    /// Clears all form fields
    function clear_item_form_data() {
        $("#item_order_id").val("");
        $("#item_product_id").val("");
        $("#item_price").val("");
        $("#item_quantity").val("");
    }

    // ****************************************
    // Create an item
    // ****************************************

    $("#item_create-btn").click(function () {
        let order_id = $("#item_order_id").val();
        let product_id = $("#item_product_id").val();
        let price = $("#item_price").val();
        let quantity = $("#item_quantity").val();
        
        let data = {
            "order_id": order_id,
            "product_id": product_id,
            "price": price,
            "quantity": quantity
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: `/orders/${order_id}/items`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_item_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update an order
    // ****************************************

    $("#item_update-btn").click(function () {

        let order_id = $("#item_order_id").val();
        let product_id = $("#item_product_id").val();
        let price = $("#item_price").val();
        let quantity = $("#item_quantity").val();
        
        let data = {
            "order_id": order_id,
            "product_id": product_id,
            "price": price,
            "quantity": quantity
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/orders/${order_id}/items/${product_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_item_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve an order
    // ****************************************

    $("#item_retrieve-btn").click(function () {

        let order_id = $("#item_order_id").val();
        let product_id = $("#item_product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/orders/${order_id}/items/${product_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_item_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_item_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete an order
    // ****************************************

    $("#item_delete-btn").click(function () {

        let order_id = $("#order_id").val();
        let product_id = $("#item_product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/orders/${order_id}/items/${product_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_item_form_data()
            flash_message("Item has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#item_clear-btn").click(function () {
        $("#item_order_id").val("");
        $("#flash_message").empty();
        clear_item_form_data()
    });

    // ****************************************
    // Search for a order
    // ****************************************

    $("#item_search-btn").click(function () {
        let order_id = $("#order_id").val();
        let price = $("#item_price").val();
        let quantity = $("#item_quantity").val();

        let queryString = ""

        if (price) {
            queryString += 'price=' + price
        }else if (quantity) {
            queryString += 'quantity=' + quantity
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/orders/${order_id}/items?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#item_search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">Order ID</th>'
            table += '<th class="col-md-2">Product ID</th>'
            table += '<th class="col-md-2">Price</th>'
            table += '<th class="col-md-2">Quantity</th>'
            table += '</tr></thead><tbody>'
            let first_item = "";
            for(let i = 0; i < res.length; i++) {
                let item = res[i];
                table +=  `<tr id="row_${i}"><td>${item.order_id}</td><td>${item.product_id}</td><td>${item.price}</td><td>${item.quantity}</td></tr>`;
                if (i == 0) {
                    first_item = item;
                }
            }
            table += '</tbody></table>';
            $("#item_search_results").append(table);

            // copy the first result to the form
            if (first_item != "") {
                update_item_form_data(first_item)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });
})
