$(document).ready(function () {
    let a = window.location.search.split("=")
    const login_id = a[1].split('&')[0]
    const id = a[2]
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
                console.log(login_id, id)
                if (id == data[i][0]) {
                    let id = data[i][0]
                    let title = data[i][1]
                    let description = data[i][2]
                    let time = data[i][3]
                    let image = data[i][4].substring(1)
                    let feed_login_id = data[i][7]

                    let temp_html = `
                        
                        <div class="card mb-3" id="feed-box">
                            <img src=${image} class="card-img-top" alt="image">
                            <div class="card-body">
                                <h5 class="card-title" id="cardTitle">${title}</h5>
                                <p class="card-text" id="cardText">${description}</p>
                                <p class="card-text">${time}<small class="text-muted" id="cardTime"></small></p>
                                <button onclick="close_feed()" type="button" id="backbutton">Back</button>
                                 <a href="/modify">
                                <button type="button" onclick="open_modify()" class="hiddenbutton" id="editbutton">수정하기</button>
                                </a>
                                <button  type="button" onclick="deleteFeed()" class="hiddenbutton" id="deletebutton">삭제하기</button>             
                            </div>
                         </div>
                        `

                    open_feed(id, title, description)
                    $('#feed_page').append(temp_html)

                    return
                }
            }
        }
    });
}
//뒤로가기 페이지
function close_feed(){
window.history.go(-1) }

//수정페이지로 가기 + 수정기능

function open_feed(id, title, description) {
        localStorage.setItem('feed_id', id)
        localStorage.setItem('feed_title', title)
        localStorage.setItem('feed_description', description)
}
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
            window.history.go(-1)
        }
    });

}

function putFeed() {
        const f_id = document.getElementById('edit_id').innerText;
        const f_title = $("#edit_title").val();
        const f_description = $("#edit_description").val();
        modify_feed({id: f_id, title: f_title, description: f_description})
        }

        //삭제 기능

function delete_feed(id){

    $.ajax({
        type: 'POST',
        url: '/api/delete',
        data: {id: id},
        success: function(response){
            alert(response)
            window.location.href="/"
        }
    });

}

function deleteFeed() {
    if (confirm("정말로 삭제하시겠습니까?")){
        const f_id = localStorage.getItem('feed_id')
        delete_feed(f_id)
    }
}