// $(document).ready(function () {
//     var page = 2;
//     const $container = get('#container')

//     $(window).scroll(function() {
//         if ($(window).scrollTop() == $(document).height() - $(window).height()) {
//         console.log(++page);
//         $container.append('<article class="feed"></article>');
        
//         }
//     });
// });


window.onscroll = function(ev) {
    let temp_html = `<article class="feed"></article>`
    const {scrollTop, scrollHeight, clientHeight} = document.documentElement
    if (scrollTop + clientHeight >= scrollHeight - 100) {
    // if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
    //     console.log(window.innerHeight)
    //     console.log(window.window.scrollY)
        // console.log(scrollHeight)
        $('#container').append(temp_html)
    }
};