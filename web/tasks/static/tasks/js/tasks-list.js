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
