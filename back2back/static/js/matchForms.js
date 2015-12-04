$(function() {
    $('form').on('submit', function(e) {
        e.preventDefault();
        var form = $(this);
        var formWrapper = form.closest('td');
        var match = form.closest('tr');
        formWrapper.removeClass('error');
        form.removeClass('saved');
        form.addClass('saving');
        $.post(form.attr('action'), form.serialize(), function(data) {
            data = JSON.parse(data);
            form.removeClass('saving');
            form.addClass('saved');
            match.find('td[data-archer]').removeClass('winner');
            if (data && data.archer_1 === 2) {
                match.find('td[data-archer=1]').addClass('winner');
            }
            if (data && data.archer_2 === 2) {
                match.find('td[data-archer=2]').addClass('winner');
            }
        }).fail(function() {
            form.removeClass('saving');
            formWrapper.addClass('error');
        });
    });
});
