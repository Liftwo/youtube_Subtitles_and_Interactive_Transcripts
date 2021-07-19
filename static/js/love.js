let clicks = 0;
let like_count = 0

$(document).ready(function (){
    let like_count = document.getElementById("like_total").innerText;

    $('.for_test').text(like_count);
});

$(document).ready(function () {
    $('.btn-link').click(function () {
        let like_count = document.getElementById("like_total").innerText;

        if (clicks == 0) {
            $("#like-tag").attr("src", tag_pink);
            clicks++;
            let c = parseInt(like_count) + 1;
            $('.like_total').text(c);
        } else {
            $("#like-tag").attr("src", tag_svg);
            clicks--;
            let c = parseInt(like_count) - 1;
            $('.like_total').text(c);
        }
    let likes = document.getElementById("like_total").innerText;
    $.ajax({
        type:"POST",
        data:{likes:likes},
        headers: { "X-CSRFToken": '{{csrf_token}}' },
        });
    });
})
