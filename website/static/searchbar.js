/**
 * Created by BigFlower on 16/11/7.
 */
'use strict';


function updateSuggestBar(suggestElem, values) {
    if (values instanceof Array) {
        var ul = document.createElement('ul');

        for (var i = 0; i < values.length; ++i) {
            var li = document.createElement('li');
            li.textContent = values[i];
            ul.appendChild(li);
        }

        // assert only one child remains
        while(suggestElem.childElementCount > 1){
            suggestElem.removeChild(suggestElem.firstChild);
        }

        if(suggestElem.childElementCount == 1) {
            setTimeout(function () {
                suggestElem.removeChild(suggestElem.firstChild);
            }, 100);
        }
        suggestElem.appendChild(ul);
    }
}

window.addEventListener('load', function () {
    // var form = document.querySelector("form.searchbar");
    var input = document.querySelector("#textForm > input.keyword");
    var suggest = document.querySelector('#textForm > .suggest');


    // input.addEventListener('keydown', function (event) {
    //     if (event.keyCode == 13) {
    //         form.submit();
    //     }
    // });

    // suggest.addEventListener('click', function (event) {
    //     input.value = event.target.textContent;
    //     form.submit();
    // });



    input.addEventListener('input', function (e) {
        var val = e.target.value;
        if (val == "") {
            return
        }

        clearTimeout(e.target.throttleId);
        e.target.throttleId = setTimeout(function () {
            jQuery.ajax('http://suggestion.baidu.com/su', {
                type: "GET",
                async: true,
                dataType: "jsonp",
                jsonp: "cb",
                data: {"wd": val}
            }).done(function (data) {
                updateSuggestBar(suggest, data.s); // s is defined by baidu
            }).fail(function (err) {
                console.log(err);
            });
        }, 400);
    });

    document.addEventListener('click', function(){
        suggest.innerHTML = '';
    });

    window.addEventListener('scroll', function(){
        suggest.innerHTML = '';
    });


    // searchType.addEventListener('click', function () {
    //     var type = flipText(searchType, 'Abc', 'Img', 'flip1', 'flip2');
    //     searchTypeInput.setAttribute('value', type == 'Abc' ? 'text' : 'image');
    // });
});