
function checkURL() {
    var x = document.forms["shortener"]["long_url"].value;
    if (x == "") {
        alert("URL cannot be blank12 ");
        return false;
    }

    var pattern = new RegExp('^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$');

    if (!pattern.test(x)) {
        alert("Please enter a valid url");
            return false;
    }
}
$("#submitURL").click(function(e)   
{
    e.preventDefault();
    var x = document.forms["shortener"]["long_url"].value;
    if (x == "") {
        alert("URL cannot be blank");
        return false;
    }
    var re = /^(http[s]?:\/\/){0,1}(www\.){0,1}[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,5}[\.]{0,1}/;
    //var pattern = new RegExp('^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$');

    if (!re.test(x)) {
        alert("Please enter a valid url");
            return false;
    }


    $.ajax({
        
        type: 'GET',
        url: '/add',
        data: { long_url: x },
        beforeSend: function () {
            $('#return_url').css('display','none');
            $('#loader').css('display','block');
            $('#shortener').css('display','none');
            

          },
        complete: function () {
            $('#loader').css('display','none');
          },
        success: function(data){
            var url = '<a href = https://krop.xyz/' + data.hash_str+ ' target="_blank">krop.xyz/' + data.hash_str + '</a>'
            $('#return_url').html(url).css('display','block');
            $('#copyURL').css('display','block');
            $('#reload').css('display','block');
        }
    });
    
});


$(document).on('click', '#copyURL', function() { 
    var range = document.createRange();
    range.selectNode(document.getElementById("return_url"));
    window.getSelection().removeAllRanges(); // clear current selection
    window.getSelection().addRange(range); // to select text
    document.execCommand("copy");
    window.getSelection().removeAllRanges();// to deselect
    alert("Link copied");
});

function copyToClipboard(element) {
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val($(element).text()).select();
    document.execCommand("copy");
    $temp.remove();
  }

