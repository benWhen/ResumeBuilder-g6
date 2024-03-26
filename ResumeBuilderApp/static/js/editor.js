$(function () {
    var lastFocusValue = '';
    var focusState = 0;

    var changeWithRepeats = function (command, newestValue){
        document.execCommand(command, false, newestValue);
    };

    $('.editorSelect').click (function () {
        if (focusState == 1){
            focusState = 2;
            return;
        } else if (focusState == 2){
            $(this).blur();
        }
    }).focus(function () {
        focusState = 1;
        lastFocusValue = $(this).val();
    }).blur(function () {
        focusState = 0;
        if ($(this).val() == lastFocusValue) {
            changeWithRepeats(this.id, $(this).val());
        }
    }).change (function () {
        changeWithRepeats(this.id, $(this).val());
    });
});

function buttonSelection(event){
    event.preventDefault();
    document.execCommand(this.id);
}

$(".editorButton").mousedown(buttonSelection);

console.log(document.getElementById('resume'))
document.getElementById('resume').addEventListener('submit', function() {
    var content = document.getElementById('maintextarea').innerHTML;
    console.log(content);
    document.getElementById('data').value = content;
    console.log(document.getElementById('data').value)
});
// how to pass arguments, if ever needed:
//$(".editorButton").mousedown({command: $(this).id}, buttonSelection);
