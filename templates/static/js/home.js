$(document).ready(function() {

});

function delete_file(file_id) {
    console.log('deleting file ' + file_id);
    let trow = $('#tr' + file_id);

    $.ajax({
        type: 'POST',
        cache: false,
        data: {'file_id': file_id},
        url: '/file/delete/',
        error: function(xhr, status, e) {
            alert(xhr + ' ' + status + ' ' + e);
        },
    }).done(function(response) {
        trow.remove();
    });
}