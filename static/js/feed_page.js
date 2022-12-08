$(document).ready(function () {
    let a = window.location.search.split("=")[1].split("&")
    const login_id = a[0]
    const id = a[1]

    feed_page(login_id, id)
});


function feed_page(login_id, id) {
    $.ajax({
        type: 'GET',
        url: `/feed_page/${login_id}/${id}`,
        data: {},
        dataType: 'json',
        success: function (data) {

            for (let i = 0; i < data.length; i++) {
                if (id == data[i][0]) {
                    let id = data[i][0]
                    let title = data[i][1]
                    let description = data[i][2]
                    let time = data[i][3]
                    let image = data[i][4].substring(1)
                    let login_id = data[i][7]

                    let temp_html = `
                        <div class="card mb-3" id="feed-box">
                            <img src=${image} class="card-img-top" alt="image">
                            <div class="card-body">
                                <h5 class="card-title" id="cardTitle">${title}</h5>
                                <p class="card-text" id="cardText">${description}</p>
                                <p class="card-text">${time}<small class="text-muted" id="cardTime"></small></p>
                                <button onclick="close_feed()" type="button" id="backbutton">Back</button>
                            </div>
                         </div>`
                    $('#feed_page').append(temp_html)
                    return
                }
            }
        }
    });
}