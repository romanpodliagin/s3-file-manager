$(document).ready(function() {
    $('.alert').alert();

});

function create_dir() {
    let dir_name = $('#dir_name').val();
    let alert_file_errors = $('#alert_create_dir_errors');

//    console.log('create dir ' + dir_name);

    $.ajax({
        type: 'POST',
        cache: false,
        data: {'dir_name': dir_name},
        url: '/dirs/create/',
        error: function(xhr, status, e) {
            alert_file_errors.html(xhr.responseJSON.msg);
            alert_file_errors.show('slow').delay(3000).hide('slow');
        },
    }).done(function(response) {
        console.log('success');
        window.location.href = '/';
    });
}