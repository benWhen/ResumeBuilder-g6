$(function () {
    var lastFocusValue = '';
    var focusState = 0;

    var changeWithRepeats = function (command, newestValue){
        document.execCommand(command, false, newestValue);
        $('#mainTextArea').focus();
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
    $('#mainTextArea').focus();
}


// Event connections

$(".editorButton").mousedown(buttonSelection);

$(document).on('keydown', '#mainTextArea', function(event){

    // Tab is keyCode 9
    if(event.keyCode == 9){
                    document.execCommand('insertHTML', false, '&#009');
                    event.preventDefault();
                    $('#mainTextArea').focus();
    }
});

//gets html from div and adds it to a hidden input element also prompts user for resume name
document.getElementById('resume').addEventListener('submit', function() {
    var content = document.getElementById('mainTextArea').innerHTML;
    document.getElementById('data').value = content;
    document.getElementById('resumeName').value = prompt("Enter a name for your resume(leave blank for default name): ");
});

// New page attempt and failure:

// function refocusText(event) {
//     $(event.target).find("#textDiv").focus();
// }

// function getPageByNumber(pageNum){
//     var children = $("#textAreaContainer").children();
//     for (var i = 0; i < children.length; i++) {
//         var tableChild = children[i];
//         // Do stuff
//         if (parseInt($(tableChild).attr('data-pageNum')) == pageNum) {
//             return tableChild;
//         }
//     }
// }

// function setCaretPosition(element, offset){
//     var range = document.createRange();
//     var sel = window.getSelection();
//
//     range.setStart(element.childNodes[0], offset);
//     range.collapse(true);
//
//     sel.removeAllRanges();
//     sel.addRange(range);
// }


// function checkNewPage(event){
//     var textDiv = event.target;
//     var parent = $(textDiv).parent()[0];
//     var pageNum = parseInt($(parent).attr('data-pageNum'));
//     var heightStr = $(textDiv).css('height').replace('px','');
//     var height = parseInt(heightStr);
//     if (height > 880) {
//         event.preventDefault();
//         var nextPage = getPageByNumber(pageNum + 1);
//         if (nextPage != null) {
//             console.log("Page exists");
//             $(nextPage).find("#textDiv").focus();
//         } else {
//             var newPage = parent.cloneNode(true);
//             var newTextDiv = $(newPage).find("#textDiv")
//             $(newPage).attr('data-pageNum', pageNum + 1);
//             $(newTextDiv).html("");
//             $("#textAreaContainer").append(newPage);
//             // Event Setup
//             $(newPage).bind("keydown click focus", refocusText);
//             $(newTextDiv).bind("input", checkNewPage);
//             $(newTextDiv).bind("keydown", checkPageDeletion);
//             $(newPage).find("#textDiv").focus();
//         }
//     }
// }
//
// function checkPageDeletion(event){
//     var target = event.target;
//     var parentList = $(textDiv).parent();
//     var parent = parentList[parentList.length - 1]
//     var pageNum = parseInt($(parent).attr('data-pageNum'))
//     if (
//         event.keyCode == 8 &&
//         pageNum != 1 &&
//         $(target).html().length == 0
//     )
//     {
//         previousPage = getPageByNumber(pageNum - 1);
//         parent.remove();
//         var prevTextDiv = $(previousPage).find("#textDiv")[0];
//         console.log(prevTextDiv.text());
//         setCaretPosition(prevTextDiv, $(prevTextDiv).text().length);
//     }
// }