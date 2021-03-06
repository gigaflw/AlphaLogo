/*
* @Author: GigaFlower
* @Date:   2016-12-23 23:12:23
* @Last Modified by:   GigaFlower
* @Last Modified time: 2017-01-12 03:19:56
*/

'use strict';

var divSearch = document.getElementById("search");
var divMatch = document.getElementById("match");
var idBrowse = document.getElementById("browse");
var idLogo = document.getElementById("logo");
var idTextfield = document.getElementById("textfield");
var idTypeSearch = document.getElementById("typeSearch");
var idInputSearch = document.getElementById("inputSearch");
var idInputMatch = document.getElementById("inputMatch");
var idTitle = document.getElementById("title");
var idEnterpriseName = document.getElementById("enterpriseName");
var idNColors = document.getElementById("nColors");
var idSaturation = document.getElementById("saturation");
var idBrightness = document.getElementById("brightness");
var idIndustry = document.getElementById("industry");
var idPreviewImg = document.getElementById("previewImg");
var idImgSubmit = document.getElementById("imgSubmit");
var idCurrentPointer = document.getElementById("currentPointer");

var divAdvancedSearch = document.getElementById("advanced");
var idAdvancedSearchPanel = document.getElementById("advancedSearchPanel");
var advancedColorNum2 = document.getElementById("colorNum2");
var advancedColorNum3 = document.getElementById("colorNum3");
var advancedColorNum4 = document.getElementById("colorNum4");
var advancedColorNum5 = document.getElementById("colorNum5");
var advancedColorNumMore = document.getElementById("colorNumMore");
var advancedIndustryProfit = document.getElementById("industryProfit");
var advancedIndustryOrganization = document.getElementById("industryOrganization");
var advancedIndustryEntertainment = document.getElementById("industryEntertainment");
var advancedIndustryFestival = document.getElementById("industryFestival");
var advancedIndustryTeam = document.getElementById("industryTeam");
var advancedIndustryOthers = document.getElementById("industryOthers");
var advancedSaturationLow = document.getElementById("saturationLow");
var advancedSaturationMiddle = document.getElementById("saturationMiddle");
var advancedSaturationHigh = document.getElementById("saturationHigh");
var advancedBrightnessLow = document.getElementById("brightnessLow");
var advancedBrightnessMiddle = document.getElementById("brightnessMiddle");
var advancedBrightnessHigh = document.getElementById("brightnessHigh");
var advancedEnterpriseName = document.getElementById("advancedEnterpriseName");

window.addEventListener('load', function(){
    modeSearch();
    advancedSearchTypeInitialization();
});

divSearch.addEventListener("click", function(){
    modeSearch();
})

divMatch.addEventListener("click", function() {
    modeMatch();
})

divAdvancedSearch.addEventListener("click", function() {
    switchAdvancedSearch();
})

idBrowse.addEventListener("click", function() {
    idLogo.click();
})

idImgSubmit.addEventListener("click", function() {
    setTimeout('idImgSubmit.disabled = "disabled"', 50);
})

function showTextField() {
    //idImgSubmit.click();

    var fileName = idLogo.value;
    var reg = new RegExp("\\\\\.[^\\\\]*$");
    var regFileName = reg.exec(fileName);
    regFileName = JSON.stringify(regFileName);
    if (fileName.length == 0) {
        idTextfield.value = "";
    }
    else {
        idTextfield.value = regFileName.substring(4, regFileName.length-2);
    }

    //idPreviewImg.src = "/static/uploads/upload.jpg";
}

function modeSearch() {
    divSearch.className = "currentLinkTitle";
    divMatch.className = "linkTitle";
    divAdvancedSearch.className = "passiveAdvancedTitle";
    divAdvancedSearch.style.display = "inline-block";
    idTypeSearch.value = "search";
    idInputSearch.style.display = "block";
    idInputMatch.style.display = "none";
    idTitle.className = "title";
    idAdvancedSearchPanel.style.transform = "rotateX(90deg)";
    idCurrentPointer.style.left = "32px";
}

function modeMatch() {
    divSearch.className = "linkTitle";
    divMatch.className = "currentLinkTitle";
    divAdvancedSearch.style.display = "none";
    idInputSearch.style.display = "none";
    idInputMatch.style.display = "block";
    idTitle.className = "title";
    idAdvancedSearchPanel.style.transform = "rotateX(90deg)";
    idCurrentPointer.style.left = "157px";
}

function switchAdvancedSearch() {
    if (divAdvancedSearch.className == "passiveAdvancedTitle") {
        idTypeSearch.value = "advancedSearch";
        divAdvancedSearch.className = "activeAdvancedTitle";
        idTitle.classList.toggle("up");
        idAdvancedSearchPanel.style.transform = "rotateX(0deg)";
    } else {
        idTypeSearch.value = "search";
        divAdvancedSearch.className = "passiveAdvancedTitle";
        idTitle.classList.toggle("up");
        idAdvancedSearchPanel.style.transform = "rotateX(90deg)";
    }
}

function advancedSearchTypeInitialization() {
    var advancedSearchTypeArray = new Array(advancedColorNum2, advancedColorNum3, advancedColorNum4, advancedColorNum5, advancedColorNumMore,
        advancedSaturationLow, advancedSaturationMiddle, advancedSaturationHigh, advancedBrightnessLow,
        advancedBrightnessMiddle, advancedBrightnessHigh, advancedIndustryProfit, advancedIndustryOrganization,
        advancedIndustryEntertainment, advancedIndustryFestival, advancedIndustryTeam, advancedIndustryOthers);
    for (var x=0; x<advancedSearchTypeArray.length; ++x) {
        (function(){    // js的函数闭包问题
            var i = x;
            advancedSearchTypeArray[i].addEventListener("click", function(){;
                this.classList.toggle('active')
                if (i < 5) {
                    nColorsInput(i, this);
                } else if (i < 8) {
                    saturationInput(i-5, this);
                } else if (i < 11) {
                    brightnessInput(i-8, this);
                } else if (i < 17) {
                    industryInput(i - 11, this);
                }
            });
        })();
    }
}

function enterpriseNameInput() {
    idEnterpriseName.value = advancedEnterpriseName.value;
}

function nColorsInput(n, advancedColorNum) {
    var inputNColors = idNColors.value;
    inputNColors = advancedValueModification(n, inputNColors);
    idNColors.value = inputNColors;
}

function saturationInput(n, advancedSaturationNum) {
    var inputSaturation = idSaturation.value;
    inputSaturation = advancedValueModification(n, inputSaturation);
    idSaturation.value = inputSaturation;
}

function brightnessInput(n, advancedBrightnessNum) {
    var inputBrightness = idBrightness.value;
    inputBrightness = advancedValueModification(n, inputBrightness);
    idBrightness.value = inputBrightness;
}

function industryInput(n, advancedIndustryNum) {
    var inputIndustry = idIndustry.value;
    inputIndustry = advancedValueModification(n, inputIndustry);
    idIndustry.value = inputIndustry;
}

function advancedValueModification(n, value) {
    var valueList = value.split(",");
    var nDigit = valueList[n];
    if (nDigit == "0") {
        valueList.splice(n, 1, "1");
    } else {
        valueList.splice(n, 1, "0");
    }
    value = valueList.join(",");
    return value;
}