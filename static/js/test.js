var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;

function onYouTubeIframeAPIReady() {
        player = new YT.Player('player', {
          height: '390',
          width: '640',
          videoId: 'M7lc1UVf-VE',
          events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
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
      document.getElementById("sub-ch").textContent=subtitle.text_ch;
      document.getElementById("sub-en").textContent=subtitle.text_en;
    } else{
        document.getElementById("current").textContent="";
    }
  });
};

$(document).ready(function() {
    $("#sub-en").mouseenter(function () {
    $("#sub-en").css({"background":"gray", "color":"gray"});
    })
    $("#sub-en").mouseleave(function() {
    $("#sub-en").css({"background":"", "color":""});
    })
});