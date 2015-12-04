$(function() {
    $('form').on('submit', function(e) {
        e.preventDefault();
        var form = $(this);
        formWrapper = form.closest('td');
        formWrapper.removeClass('error');
        form.removeClass('saved');
        form.addClass('saving');
        $.post(form.attr('action'), form.serialize(), function() {
            form.removeClass('saving');
            form.addClass('saved');
        }).fail(function() {
            form.removeClass('saving');
            formWrapper.addClass('error');
        });
    });
});
