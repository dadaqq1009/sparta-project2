$(document).ready(function () {
    get_feed();
});

window.onscroll = function(ev) {
    let temp_html = `<article class="feed"></article>`
    const {scrollTop, scrollHeight, clientHeight} = document.documentElement
    if (scrollTop + clientHeight >= scrollHeight - 200) {
        $('#container').append(temp_html)
    }
};

function get_feed() {
    $.ajax({
        type: "GET",
        url: "/feed",
        data: {},
        dataType: 'json',
        success: function (data) {
            for (let i = 0; i < data.length; i++) {
                let id = data[i][0]
                let title = data[i][1]
                let description = data[i][2]
                let created_at = data[i][3]
                let image = data[i][4].substring(1)
                let user_id = data[i][7]


                let temp_html = `<article class="feed">
                                  <img src=${image} alt="" />
                                  <div class="feed_text_wrap">
                                    <h4 class="feed_title">${title}</h4>
                                    <p class="feed_descript">
                                      ${description}
                                    </p>
                                  </div>
                                  <div class="feed_user">
                                    <p class="feed_user_id">${user_id}<span>${created_at}</span></p>
                                  </div>
                                </article>`
                $('#container').prepend(temp_html)
                console.log(user_id)
            }
        }
    });
}

