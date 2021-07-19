function UnescapeHTML(a) {
    a = "" + a;
    return a.replace(/&#39;/g, "'").replace(/&quot;/g, "\"").replace(/&amp;/g, "&");
}

var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function onYouTubeIframeAPIReady() {
        player = new YT.Player('player', {
          height: '360',
          width: '840',
          videoId: video_id,
          events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange,
          }
        });
      }

function onPlayerReady(event) {
    event.target.mute().playVideo();
  }

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
}

function ShowSubtitles() {
      var current_time = player.getCurrentTime();
      console.log(current_time);
      subtitles.forEach(function(subtitle, i) {

        if (current_time >= subtitle.start && current_time <= subtitle.end) {
          document.getElementById("sub-ch").textContent=UnescapeHTML(subtitle.text_ch);
          document.getElementById("sub-en").textContent=UnescapeHTML(subtitle.text_en);
          document.getElementById("sub-test").textContent=subtitle.start;
        }
      });
    };

$("span").text()

$(document).ready(function(event) {
        $("#sub-en").mouseenter(function () {
        $("#sub-en").css({"background":"", "color":""});
        player.pauseVideo();
        })
        $("#sub-en").mouseleave(function() {
        $("#sub-en").css({"background":"gray", "color":"gray"});
        player.playVideo();
        })
    });

$("#player").css("text-align", "center");

function ShowJson_dual(){
    document.getElementById("sub-test").textContent=subtitles;
}

