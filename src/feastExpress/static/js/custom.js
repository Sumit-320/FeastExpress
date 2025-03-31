let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in']},
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
}