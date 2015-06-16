var url = window.location.href;
if (url.indexOf("soccer") > -1){
    // The table relates our combination # to the stored image name
    var compType = 'soccer';
    var lookupTable =   [[1,'Bosko Balaban'],
                        [2,'Cristiano Ronaldo'],
                        [3,'Lionel Messi'],
                        [4,'Luis Suarez'],
                        [5,'Xavi Hernandez']];
}

if (url.indexOf("math") > -1){
    // The table relates our combination # to the stored image name
    var compType = 'math';
    var lookupTable =   [[1,'Blaise Pascal'],
                        [2,'Carl Gauss'],
                        [3,'Daniel Bernoulli'],
                        [4,'Guillaume l\'Hôpital'],
                        [5,'Issac Newton']];
}

if (url.indexOf("rappers") > -1){
    // The table relates our combination # to the stored image name
    var compType = 'rappers';
    var lookupTable =   [[1,'Eminem'],
                        [2,'Jay-Z'],
                        [3,'Notorious BIG'],
                        [4,'Rakim'],
                        [5,'Snoop Dogg'],
                        [6, 'Tupac Shakur']];
}

if (url.indexOf("movies") > -1){
    // The table relates our combination # to the stored image name
    var compType = 'movies';
    var lookupTable =   [[1,'Dances With Wolves'],
                        [2,'Disaster Movie'],
                        [3,'The Bank Job'],
                        [4,'The Godfather'],
                        [5,'Titanic']];
}

if (url.indexOf("musicians") > -1){
    // The table relates our combination # to the stored image name
    var compType = 'musicians';
    var lookupTable =   [[1,'Bach'],
                        [2,'Beethoven'],
                        [3,'Chopin'],
                        [4,'Mendelssohn'],
                        [5,'Mozart']];
}

if (url.indexOf("colors") > -1){
    // The table relates our combination # to the stored image name
    var compType = 'colors';
    var lookupTable =   [[1,'Black'],
                        [2,'Blue Brushed'],
                        [3,'Light Green'],
                        [4,'Purple'],
                        [5,'White']];
}

if (url.indexOf("places") > -1){
    // The table relates our combination # to the stored image name
    var compType = 'places';
    var lookupTable =   [[1,'Eiffel Tower'],
                        [2,'Leaning Tower of Pisa'],
                        [3,'Statue of Liberty'],
                        [4,'Sydney Opera House'],
                        [5,'The Pyramids']];
}

if (url.indexOf("numbers") > -1){
    // The table relates our combination # to the stored image name
    var compType = 'numbers';
    var lookupTable =   [[1,'1'],
                        [2,'120'],
                        [3,'199'],
                        [4,'1498'],
                        [5,'1703']];
}

// cache images to improve loading times
// this function is important for optimization to minimize potential lag-time
$.preLoadImages = function(urls) {
    var args_len = urls.length;
    for (var i=0; i < args_len; i++) {
        var cacheImage = document.createElement('img');
        cacheImage.src = urls[i];
    }
}

// create array of urls for .preLoadImages
var url_arr = []
for (var i=0; i<lookupTable.length; i++){
    var url = '/static/images/'+lookupTable[i][1].replace(" ", "%20")+'.jpg';
    url_arr.push(url);
}

$.preLoadImages(url_arr)

// represent images by numbers [1:N] and matchups as follows
// combinations without repition (r assumed to be 2)
function combinations(n){
    matchups = [];
    for (var i=1; i<n; i++){
        for (var j=i+1; j<=n; j++){
            matchups.push([i,j]);
        };
    };
    return matchups;
}

var matchups = combinations(5);

// Returns a random integer between min (included) and max (excluded)
// Using Math.round() will give you a non-uniform distribution!
function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min)) + min;
}

// continue the process until a selection is made from all matchups
// particularly choose matchups randomly 
// (assuming decent pseudo generation from js)
function getMatchup(matchups){
    var index = getRandomInt(0,matchups.length);
    var matchup = matchups[index];
    matchups.splice(index, 1);
    return matchup;
}

// lookup matchups in table and return indices
function lookupImage(matchup){
    return [lookupTable[matchup[0]-1], lookupTable[matchup[1]-1]]
}

//+ Jonas Raoni Soares Silva
//@ http://jsfromhell.com/array/shuffle [v1.0]
// this functions shuffles an array's order
function shuffle(o){ //v1.0
    for(var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
    return o;
};

// important global vars
var count = -1;
var TTChoose = [];
var start = 0;
var maxCount = matchups.length;
var matchArray = [];
var choices = [];

// load images according to randomly chosen matchups and change the src attr.
function loadImages(element){
    if (matchups.length){
        if (element){
            choices.push($(element).attr('value'));
        }
        var matchup = getMatchup(matchups);
        var tableVals = lookupImage(matchup);
        // randomizes the side for which an image is on
        tableVals = shuffle(tableVals);
        // record all the match orders since we have randomization enabled
        matchArray.push(tableVals);
        var img1 = '/static/images/'+tableVals[0][1].replace(" ", "%20")+'.jpg';
        $("#Img1").attr("src", img1)
        $("#Img1").attr("value", tableVals[0][1])
        $("#caption1").text(tableVals[0][1])
        var img2 = '/static/images/'+tableVals[1][1].replace(" ", "%20")+'.jpg';
        $("#Img2").attr("src", img2)
        $("#Img2").attr("value", tableVals[1][1])
        $("#caption2").text(tableVals[1][1])
        // keep track of count and update progress bar
    }
    // keep track of elapsed time for each choice
    if (count < maxCount){
        if (count == maxCount-1){
            if (element){
                choices.push($(element).attr('value'));
            }
        }
        count++
        $('progress').attr('value', count);
        var compStr = count + " out of  10 completed."
        $("#completed").text(compStr)
        if (count == 0){
            start = new Date();
        }
        if (count != 0){
            var elapsed = new Date() - start;
            TTChoose.push(elapsed);
            start = new Date();
        }
    }
}


function getNames(array){
    var matchupNames = [];
    for (var i=0; i<array.length; i++){
        matchupNames.push([array[i][0][1], array[i][1][1]]);
    }
    return matchupNames;
}


// account for initial condition on page load
// $(document).ready("load",
//     loadImages()
// )

// var clicks = null
// var username = null
// $("#start").click(
//     function(){
//         loadImages()
//         clicks = clicks + 1
//         if (clicks==1){
//             start = new Date();
//             username = $("#username").val()
//         }
//     }
// )

var clicks = null
var username = null
$("#start").click(
    function(){
        username = $("#username").val()
        $(".removeAfterEnter").remove()
        $(".download").val("Ready Go!")
        $(".download").css("font-weight", 800)
        $(".modalHeading").css("color", "blue")
        $(".download").attr("id", "end")
        $("#end").click(
            function(){
                $(".modalDialog").remove();
                loadImages()
                clicks = clicks + 1
                if (clicks==1){
                    start = new Date();
                }
            }
        )
    }
)



// on an image click we will change the matchup (handled in html)

// on the last choice, inititate ajax call to transfer data to server
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
$('.Images').click(function(){
    if (count == maxCount){
       var  matchupNames = getNames(matchArray);
        $.ajax({
          type: "POST",
          url: "/complete/",
          data: {
              'compType': compType,
              'matchupNames': JSON.stringify(matchupNames),
              'choices': JSON.stringify(choices),
              'TTChoose': JSON.stringify(TTChoose),
              'Time': JSON.stringify(Date()),
              'username': username,
              'csrfmiddlewaretoken': csrftoken
            },
            success: surveySuccess,
            dataType: 'html'
        });
    };
});

// handles the returned html/data from Django
// clears existing body, then replaces it with returned html
function surveySuccess(data, textStatus, jqXHR){
    data = $.parseHTML(data);
    $("body").empty();
    for(var i=0; i<data.length; i++){
        $("body").append(data[i])
    }
    getTopChoices();
}

// get mode including ties of an array
function getMode(store){
    var frequency = {};  // array of frequency.
    var max = 0;  // holds the max frequency.
    var result = [];   // holds the max frequency element.
    for (var v=0; v<store.length; v++) {
            frequency[store[v]]=(frequency[store[v]] || 0)+1; // increment frequency.
            if(frequency[store[v]] > max) { // is this frequency > max so far ?
                    max = frequency[store[v]];  // update max.
                    result = [];
                    result.push(store[v]);          // update result.
            }
            else if(frequency[store[v]] == max){
                result.push(store[v]);
            }
            else {
                continue
            }
    }
    return result
}

function getTopChoices(mode){
    var first = getMode(choices);
    // if (first).length == 1){
    //     $("#test1").text(first[0])
    // }
    $("#test1").text(first[0])
    var index = 1
    while (index>-1){
        index = choices.indexOf(first[0]);
        if (index>-1){
            choices.splice(index, 1);
        };
    };
    var second = getMode(choices)
    $("#test2").text(second[0])
}
    