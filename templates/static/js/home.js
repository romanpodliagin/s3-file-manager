$(document).ready(function() {
    $('.alert').alert();

    let alert_file_errors = $('#alert_file_errors');
    alert_file_errors.hide();

    $('#RenameModal').on('shown.bs.modal', function () {
        $('#myInput').trigger('focus')
        });
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

function rename_file(file_id) {
    let file_name = $('#new_file_name').val()
    let file_name_ext = $('#new_file_name_ext').text();
    let new_file_name = file_name.concat(file_name_ext);
    let alert_file_errors = $('#alert_file_errors');

//    console.log('renaming file ' + file_id + ' to ' + new_file_name);

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
        window.location.href = '/';
    });
}