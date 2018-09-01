// $('form').submit(function (evt) {
//    evt.preventDefault(); //prevents the default action
// });

$('.user-item__delete-button').on('click', function(event) {
    event.preventDefault();
    var element = $(this);
    var task_id = $('.task-detail').attr("data-task-id");
    $.ajax({
        url: '/tasks/' + task_id +'/delete_permission',
        type: 'POST',
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            user_id: element.attr("data-user-id"),
            redirect: '/tasks/' + task_id
        },
    }).done(function (data) {
        if (data.success) {
            window.location.href = data.url;//go to another web page
        }
    });
});

$('.users__add-user__form').submit(function(e) {// added user
    e.preventDefault();
    var task_id = $('.task-detail').attr("data-task-id");
    $.ajax({
        url: '/tasks/' + task_id +'/share_permission',
        type: 'POST',
        data: {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            user: $('.add-user__form__input').val()
        },
    }).done(function (data) {
        if (data.success) {
            window.location.href = data.url;
        } else if (!data.success) {
            $('.add-user__form__input').addClass('is-invalid')
        }
    });
});