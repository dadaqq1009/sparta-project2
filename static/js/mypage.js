
    function my_feed() {

    $.ajax({
        type: 'GET',
        url: `/api/mypages`,
        data: {},
        dataType: 'json',
        success: function (data) {
            for (let i = 0; i < data.length; i++) {
                let id = data[i][0]
                let title = data[i][1]
                let description = data[i][2]
                let time = data[i][3]
                let image = data[i][4].substring(1)

                let temp_html =
                    `
                         <div class="card mb-3" id="feed-box" onclick="open_feed('${id}','${title}','${description}','${time}')">
                            <img src= ${image} class="card-img-top" alt="image">
                            <div class="card-body">
                                <h5 class="card-title" id="feedTitle">Title: ${title}</h5>
                                <p class="card-text" id="feedText">${description}</p>
                                <p class="card-text"><small class="text-muted">Last updated: ${time}</small></p>
                            </div>
                         </div>
                        `

                $(`#section`).prepend(temp_html)
                console.log(image)

            }

        }
    })}



//고처야 되는 상세페이지 부분

    let temp_html_feed = `
    <div className="card mb-3" id="feed-box">
        <img src="..." className="card-img-top" alt="image">
            <div className="card-body">
                <h5 className="card-title" id="cardTitle"></h5>
                <p className="card-text" id="cardText"></p>
                <p className="card-text"><small className="text-muted" id="cardTime"></small></p>
                <button className="btn btn-primary" onClick="close_feed()" id="backButton" role="button">back</button>
                <a className="btn btn-primary" id="editButton" href="/modify" role="button">edit</a>
                <button className="btn btn-primary" id="deleteButton" onclick="deleteFeed()" role="button">delete</button>
            </div>
    </div>
    `

let selectedId
    function open_feed(id, title, description, time) {
    selectedId = id
    $('#section').empty()
    $('#section').append(temp_html_feed)
        document.getElementById('cardTitle').innerText += title
        document.getElementById('cardText').innerText += description
        document.getElementById('cardTime').innerText += time
        localStorage.setItem('feed_id', id)
        localStorage.setItem('feed_title', title)
        localStorage.setItem('feed_description', description)
        localStorage.setItem('feed_time', time)
}


    function close_feed(){
    window.location.reload()
}

//삭제 부분

function delete_feed(id){

    $.ajax({
        type: 'POST',
        url: '/api/mypages',
        data: {id: id},
        success: function(response){
            alert(response)
            window.location.href='/mypage'
        }
    });
    console.log(id)
}

function deleteFeed() {
        const f_id = localStorage.getItem('feed_id')
        delete_feed(f_id)
    console.log(f_id)
        }

//modify 페이지
function open_modify(){
     document.getElementById('edit_id').innerText += localStorage.getItem('feed_id')
    document.getElementById('edit_title').innerText += localStorage.getItem('feed_title')
    document.getElementById('edit_description').innerText += localStorage.getItem('feed_description')
}

function modify_feed(data){
    const {id, title, description} = data
    $.ajax({
        type: 'POST',
        url: '/api/modify',
        data: {id: id, title: title, description: description},
        success: function(response){
            alert(response)
            window.location.href='/mypage'
        }
    });
    console.log(data)
}



function putFeed() {
        const f_id = document.getElementById('edit_id').innerText;
        const f_title = $("#edit_title").val();
        const f_description = $("#edit_description").val();
        modify_feed({id: f_id, title: f_title, description: f_description})
    // console.log(f_id, f_title, f_description)
        }


