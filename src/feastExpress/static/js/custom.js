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
                console.log(response)
            }
        })
    })
    
    // cart qty 
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
    })
});

