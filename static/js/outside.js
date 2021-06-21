var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;

function onYouTubeIframeAPIReady() {
  player = new YT.Player('player', {
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onPlayerStateChange
    }
  });
}

function onPlayerReady(event) {
    event.target.mute().playVideo();
  };

function onPlayerStateChange(event) {
  var Update;
  if (event.data == YT.PlayerState.PLAYING) {
    Update = setInterval(function() {
      ShowSubtitles()
    }, 100);
  } else {
    clearInterval(Update);
  };
  console.log(event.data)
};


function ShowSubtitles() {
  var current_time = player.getCurrentTime();
  subtitles.forEach(function(subtitle, i) {

    if (current_time >= subtitle.data-start && current_time <= subtitle.data-end) {
      document.getElementById("sub").textContent=subtitle.text;
    } else {
      subtitle.dom.classList.add("youtube-marker-current");
    }
  });
};


var element = document.getElementById('sub-ch');
  element.onclick = function() {
      // Get Data Attribute
      element.dom.classList.add("cover-subtitles");
    }

function CoverSubtitles() {
                        var element = document.getElementById("sub-ch");
                        if (element.style.display === "none") {
                            element.style.display = "block";
                        } else {
                            element.style.display = "none";
                        }
                    };

function CoverSubtitles() {
                        var element = document.getElementById("sub-ch").value;
                        if (element != "") {
                            document.getElementById("sub-ch").innerHTML = "____________";
                        } else {
                            document.getElementById("sub-ch").innerHTML = element;
                        }
                    };