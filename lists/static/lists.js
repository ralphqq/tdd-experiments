window.Superlist = {};
window.Superlist.initialize = function() {
    $('input[name="text"]').keydown(function() {
        $('.has-error').hide();
    });
};