$(document).ready(function () {
    const login_id = window.location.search.split("?")[1]
    console.log(window.location.href)
    mypage(login_id);
});



    function mypage(login_id) {

    $.ajax({
        type: 'GET',
        url: `/api/mypage`,
        data: {},
        dataType: 'json',
        success: function (data) {
            for (let i = 0; i < data.length; i++) {

                let id = data[i][0]
                let title = data[i][1]
                let description = data[i][2]
                let time = data[i][3]
                let image = data[i][4].substring(1)
                let feed_login_id = data[i][7]

                let temp_html =
                    `<a href="/feed_page?${feed_login_id}?${id}">
                         <div class="card mb-3" id="feed-box" onclick="open_feed('${id}','${title}','${description}','${time}')">
                            <img src= ${image} class="card-img-top" alt="image">
                            <div class="card-body">
                                <h5 class="card-title" id="feedTitle">Title: ${title}</h5>
                                <p class="card-text" id="feedText">${description}</p>
                                <p class="card-text"><small class="text-muted">Last updated: ${time}</small></p>
                            </div>
                         </div>
                        `

                if (login_id == feed_login_id){
                    $('#container').prepend(temp_html)
                }
            }
        }
    })}



