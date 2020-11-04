$(document).ready(function() {
    load_dir_names();
});

function load_dir_names () {
    $.getJSON( '/dirs/list/', function( data ) {
//        console.log(data.results);
        $.each( data.results, function( index, item ) {
            console.log(item);
            $('#id_directory').append(`<option value="` + item.id + `">` + item.name + `</option>`) });
    });
}
