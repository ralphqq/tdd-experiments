window.Superlist = {};
window.Superlist.initialize = function() {
        $('input[name="text"]').on('keydown click', function() {
        $('.has-error').hide();
    });
};