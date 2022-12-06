window.onscroll = function(ev) {
    let temp_html = `<article class="feed"></article>`
    const {scrollTop, scrollHeight, clientHeight} = document.documentElement
    if (scrollTop + clientHeight >= scrollHeight - 200) {
        $('#container').append(temp_html)
    }
};

function get_feed() {
    $.ajax({
        type: "POST",
        url: "/feed",
        data: {},
        success: function (response) {
            let rows = response['guests']
            for (let i = 0; i < rows.length; i++) {
                let cnt = rows[i]['cnt']
                let guestName = rows[i]['guestName']
                let guestMbti = rows[i]['guestMbti']
                let guestComment = rows[i]['guestComment']

                let temp_html = `<div class="card">
                                    <figcaption class="blockquote-footer">
                                        ${guestMbti}<cite title="Source Title">${guestName}</cite>
                                    </figcaption>
                                    <blockquote class="blockquote">
                                        <p>${guestComment}</p>
                                    </blockquote>
                                    <button onclick="teamdelete_comment(${cnt})" type="button" class="btn del_btn btn-dark">삭제하기</button>             
                                </div>`
                $('#comm-list').append(temp_html)
            }
        }
    });
}

