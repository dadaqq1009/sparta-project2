$(document).ready(function () {
    const login_id = window.location.search
    console.log(window.location.href)
    // my_feed(login_id);
});

// function my_feed() {
//     console.log("my_feed: ",login_id)
//     $.ajax({
//         type: 'GET',
//         url: `/${login_id}`,
//         data: {},
//         dataType: 'json',
//         success: function (data) {
//             for (let i = 0; i < data.length; i++){
//                 let id = data[i][0]
//                 let title = data[i][1]
//                 let description = data[i][2]
//                 let time = data[i][3]
//                 let image = data[i][4].substring(1)
//
//                 let temp_html =
//                     `
//                      <div class="card mb-3" id="feed-box" onclick="open_feed('${id}','${title}','${description}', '${time}')">
//                         <img src= ${image} class="card-img-top" alt="image">
//                         <div class="card-body">
//                             <h5 class="card-title" id="feedTitle">Title: ${title}</h5>
//                             <p class="card-text" id="feedText">${description}</p>
//                             <p class="card-text"><small class="text-muted">Last updated: ${time}</small></p>
//                         </div>
//                      </div>
//                     `
//                 $(`#content`).prepend(temp_html)
//                 console.log(image)
//
//             }
//
//         }})}


// ********************************************************************************
//
// function open_feed(id, title, description, time) {
//     $('#section').empty()
//     $('#section').append(temp_html_feed)
//     document.getElementById('cardTitle').innerText += title
//     document.getElementById('cardText').innerText += description
//     document.getElementById('cardTime').innerText += time
//
//
// }
//
//
// function close_feed(){
//     window.location.reload()
// }
//
// let temp_html_feed = `
//                      <div class="card mb-3" id="feed-box">
//                         <img src="..." class="card-img-top" alt="image">
//                         <div class="card-body">
//                             <h5 class="card-title" id="cardTitle"></h5>
//                             <p class="card-text" id="cardText"></p>
//                             <p class="card-text"><small class="text-muted" id="cardTime"></small></p>
//                             <button onclick="close_feed()" type="button" id="backbutton">Back</button>
//                         </div>
//                      </div>
//
//
//                 `