$(document).ready(function() {
    $('.alert').alert();
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

function delete_dir(dir_id) {
    console.log('deleting dir ' + dir_id);
    let trow = $('#dir_' + dir_id);

    $.ajax({
        type: 'POST',
        cache: false,
        data: {'dir_id': dir_id},
        url: '/dirs/delete/',
        error: function(xhr, status, e) {
            alert(xhr + ' ' + status + ' ' + e);
        },
    }).done(function(response) {
        trow.remove();
    });
}
