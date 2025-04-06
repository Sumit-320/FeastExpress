let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        componentRestrictions: {'country': ['in']}, // currently for India only!
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}
function onPlaceChanged (){
    var place = autocomplete.getPlace(); //it retrieves the place object (details) for the selected place.

    // If the place is not valid
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{// If the place is valid (i.e., the user selects a suggestion) 
        // console.log('place name=>', place.name)
    }
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value 

    // this function is to auto-fill the form values in my-restaurant page from google geocoding API
    geocoder.geocode({'address':address},function(results,status){
        if(status==google.maps.GeocoderStatus.OK){
            var latitude = results[0].geometry.location.lat()   // lat from api call 
            var longitude = results[0].geometry.location.lng()
            $('#id_latitude').val(latitude)
            $('#id_longitude').val(longitude)
             // instead of manually assigning values, using loop
             for(var i=0; i<place.address_components.length; i++){
                for(var j=0; j<place.address_components[i].types.length; j++){
                    if(place.address_components[i].types[j] == 'country'){
                        $('#id_country').val(place.address_components[i].long_name);
                    }
                    if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                        $('#id_state').val(place.address_components[i].long_name);
                    }
                    if(place.address_components[i].types[j] == 'locality'){
                        $('#id_city').val(place.address_components[i].long_name);
                    }
                    if(place.address_components[i].types[j] == 'postal_code'){
                        $('#id_pin').val(place.address_components[i].long_name);
                    }else{
                        $('#id_pin').val("");
                    }
                }
            }
        }
    })
}


$(document).ready(function(){
    $('.add_to_cart').on('click',function(e){
        e.preventDefault();
        // add to cart takes food id and url, then sends request to url=$... using AJAX get request 
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        data = {
            food_id: food_id,
        }

        $.ajax({
            type: 'GET',
            url: url,  // url is addToCart views.py and it gets HttpResonse
            data:data,
            success:function(response){
            // refer to views.py
            console.log(response)
            if(response.status=='login_required'){
                swal(response.message,'','info').then(function(){
                    window.location = '/login'; // redirects to login page on clicking 'OK'
                })
            }
            if(response.status=='Failed'){
                swal(response.message,'','error')
            }else{
                $('#cart_counter').html(response.cart_counter['cart_count']);
                $('#qty-'+food_id).html(response.qty);

                // checkout sum
                applyCartAmount(
                    response.cart_amount['subtotal'],
                    response.cart_amount['tax'],
                    response.cart_amount['grand_total'],
                )
            }
            } 
        })
    })
    $('.decrease_cart').on('click',function(e){
        e.preventDefault();
        // add to cart takes food id and url, then sends request to url=$... using AJAX get request 
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');

        $.ajax({
            type: 'GET',
            url: url,  // url is addToCart views.py and it gets HttpResonse
            cart_id: cart_id,
            success:function(response){
            // refer to views.py
                if(response.status=='login_required'){
                    swal(response.message,'','info').then(function(){
                        window.location = '/login'; // redirects to login page on clicking 'OK'
                    })
                }
                if(response.status=='Failed'){
                    swal(response.message,'','error')
                }else{

                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);
                    applyCartAmount(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total'],
                    )
                    if(window.location.pathname=='cart/'){
                        removeCartItem(response.qty,cart_id);
                        checkEmptyCart();
                    }
                }
            }
        })
    })
    $('.delete_cart').on('click',function(e){
        e.preventDefault();
        // add to cart takes food id and url, then sends request to url=$... using AJAX get request 
        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        
        $.ajax({
            type: 'GET',
            url: url,  // url is addToCart views.py and it gets HttpResonse
            success:function(response){
            // refer to views.py
                
                if(response.status=='Failed'){
                    swal(response.message,'','error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    swal(response.status,response.message,"success")
                    applyCartAmount(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total'],
                    )
                    removeCartItem(0,cart_id);
                    checkEmptyCart();

                }
            }
        })
    })
    // cart qty 
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
    })
    // remove empty cart
    function checkEmptyCart(){
        var count = document.getElementById('cart_counter').innerHTML
        if(count==0){
            document.getElementById("empty-cart").style.display="block";
        }
    }
    function applyCartAmount(subtotal,taxt,grand_total){
        if(window.location.pathname=='/cart/'){
            $('#subtotal').html(subtotal)
            $('#tax').html(tax)
            $('#total').html(grand_total)
        }
    }

    function removeCartItem(cartItemQty,cart_id){
        if(cartItemQty<=0){
            document.getElementById("cart-item-"+cart_id).remove()
        }
    }
    
});

