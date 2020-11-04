$(document).ready(function() {
    $('.alert').alert();

    $('.alert').each(function( index ) {
        $(this).hide();
    });

});

function rename_file(file_id) {
    let file_name = $('#new_file_name_' + file_id).val();
    let file_name_ext = $('#new_file_name_ext_' + file_id).text();
    let new_file_name = file_name.concat(file_name_ext);

    let alert_file_errors = $('#alert_file_errors_' + file_id);

    console.log('renaming file ' + file_id + ' to ' + new_file_name);

    $.ajax({
        type: 'POST',
        cache: false,
        data: {'file_id': file_id,
                'full_file_name': new_file_name,
                'file_name': file_name},
        url: '/file/rename/',
        error: function(xhr, status, e) {
            alert_file_errors.html(xhr.responseJSON.msg);
            alert_file_errors.show('slow').delay(3000).hide('slow');
        },
    }).done(function(response) {
        console.log('success');
//        window.location.href = '/';
    });
}
