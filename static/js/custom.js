$(document).ready(function () {
    $(".increment-btn").click(function (e) {
        e.preventDefault();

        var $clickedButton = $(this);
        var $productData = $clickedButton.closest('.product_data');
        var inc_value = $productData.find('.qty-input').val();
        var value = parseInt(inc_value, 10);
        value = isNaN(value) ? 0 : value;

        var total_product_qty = parseInt($productData.find('.prod_quantity').val());
        $clickedButton.prop('disabled', false)
        if (value < total_product_qty) {
            value++;
            $productData.find('.qty-input').val(value);
        } else {
            alertify.error("Out of Stock");
//            $clickedButton.prop('disabled', true);
        }
    });


    $(".decrement-btn").click(function (e) {
        e.preventDefault();

        var $productData = $(this).closest('.product_data');
        var dec_value = $productData.find('.qty-input').val();
        var value = parseInt(dec_value, 10);
        value = isNaN(value) ? 0 : value;

        if (value > 1) {
            value--;
            $productData.find('.qty-input').val(value);
        } else {
            var product_id = $(this).closest('.product_data').find('.prod_id').val();
            console.log(product_id)
            var token = $("input[name=csrfmiddlewaretoken]").val();
            $.ajax({
                method: "POST",
                url: "delete-cart-item",
                data: {
                    'product_id': product_id,
                    csrfmiddlewaretoken: token
                },
                success: function (response) {
                    alertify.success(response.status)
                    $('.cartdata').load(location.href + " .cartdata ");

                }
            });
        }
    });


    $('.addToCartBtn').click(function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var product_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $("input[name=csrfmiddlewaretoken]").val();
        $.ajax({
            method: "POST",
            url: "/add-to-cart",
            data: {
                'product_id': product_id,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token

            },
            success: function (response) {
//                console.log(response)
                alertify.success(response.status)

            }
        });
    });

    $('.addToWishlist').click(function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $("input[name=csrfmiddlewaretoken]").val();
        $.ajax({
            method: "POST",
            url: "/add-to-wishlist",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
//                console.log(response)
                alertify.success(response.status)
            }
        });
    });

    $('.changeQuantity').click(function (e) {
        e.preventDefault();
        var $clickedButton = $(this);
        var product_id = $clickedButton.closest('.product_data').find('.prod_id').val();
        var product_qty = parseInt($clickedButton.closest('.product_data').find('.qty-input').val());
        var total_product_qty = parseInt($clickedButton.closest('.product_data').find('.prod_quantity').val());
        var prod_price = parseInt($clickedButton.closest('.product_data').find('.prod_price_hidden').text().replace(/\s+/g, " "));
        var amount = product_qty * prod_price;
        var token = $("input[name=csrfmiddlewaretoken]").val();

        if (product_qty <= total_product_qty) {
            $.ajax({
                method: "POST",
                url: "/update-cart",
                data: {
                    'product_id': product_id,
                    'product_qty': product_qty,
                    csrfmiddlewaretoken: token
                },
                success: function (response) {
                    alertify.success(response.status)
                    $clickedButton.closest('.product_data').find('.prod_price').text("Rs " + amount);
                }
            });
        } else {
            alertify.error("Out of Stock");
        }
    });


    $(document).on('click', '.delete-cart-item', function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $("input[name=csrfmiddlewaretoken]").val();
        $.ajax({
            method: "POST",
            url: "delete-cart-item",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                alertify.success(response.status)
                $('.cartdata').load(location.href + " .cartdata ");

            }
        });
    });


    $(document).on('click', '.delete-wishlist-item', function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $("input[name=csrfmiddlewaretoken]").val();
        $.ajax({
            method: "POST",
            url: "/delete-wishlist-item",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                alertify.success(response.status)
                $('.wishlistdata').load(location.href + " .wishlistdata ");

            }
        });
    });

});

