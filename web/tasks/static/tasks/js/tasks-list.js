$('.tags__button').on('click', function(event) { //эта функция делают запрос на сервер с активным тегом в теле запроса
    let element = $(this);
    $.ajax({
        url: '',
        type: 'GET',
        data: {active_tag: element.attr("data-tag")},
    })
        .done(function( data ) {
            $('.content').html(data); //меняем старый контент на новый
            $('.tags__button.active').removeClass('active'); //старую кнопку делаем не активной
            $('.tags-sidebar [data-tag=' + element.attr("data-tag") + ']').addClass('active'); // делаем активной нсажатую
        })
        .fail(function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
            console.log( "Status: " + status );
            console.dir( xhr );
        })
});

$('.tags__button').on('click', function(event) {
    let element = $(this);
    $.ajax({
        url: '',
        type: 'GET',
        data: {active_tag: element.attr("data-tag")},
    })
        .done(function( data ) {
            $('.content').html(data);
            $('.tags__button.active').removeClass('active');
            $('.tags-sidebar [data-tag=' + element.attr("data-tag") + ']').addClass('active');
        })
        .fail(function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
            console.log( "Status: " + status );
            console.dir( xhr );
        })
});

$('.user-item__delete-button').on('click', function(event) {
    event.preventDefault();
    var element = $(this);
    var task_id = $(this).attr("data-task-id");
    $.ajax({
        url: '/tasks/delete_permission/' + task_id,
        type: 'POST',
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            user_id: element.attr("data-user-id"),
            redirect: '/tasks'
        },
    }).done(function (data) {
        if (data.success) {
            window.location.href = data.url;
        }
    });
});

$('.task__status-checkbox').on('click', function (event) {
    event.preventDefault();
    var element = $(this);
    var task_id = $(this).attr("data-task-id");
    $.ajax({
        url: '/tasks/toggle_task_completion/' + task_id,
        type: 'POST',
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
        },
    }).done(function (data) {
        if (data.success) {
            element.prop('checked', !element.is(':checked'));
            console.log(element.is(':checked'));
            console.log(element.parent());
            element.parent().attr('data-status', element.is(':checked') ? 1 : 0);
        }
    });
});

$('.period-button').on('click', function(event) {
    let element = $(this);
    $.ajax({
        url: '',
        type: 'GET',
        data: {period: element.attr("data-period")},
    })
        .done(function( data ) {
            $('.content').html(data);
            $('.period-button.active').removeClass('active');
            $('.task-list__toolbox [data-tag=' + element.attr("data-period") + ']').addClass('active');
        })
        .fail(function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
            console.log( "Status: " + status );
            console.dir( xhr );
        })
});
