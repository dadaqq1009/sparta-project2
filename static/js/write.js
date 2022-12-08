function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('img-preview').src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    } else {
        document.getElementById('img-preview').src = "";
    }
}

function register_click() {
  const input_file = document.getElementById('file_form');
  console.log(input_file);
  let data = new FormData(input_file);
    console.log(data);
    const check_title = document.getElementById('txtTitle').value;
  const check_descript = document.getElementById('txtPost').value;
  // const image_check = document.getElementById('img-preview').value;
  if (check_title.length < 1) {
      alert('제목을 입력하세요');
  } else if (check_descript.length < 1) {
      alert('내용을 입력하세요');
  } else {
    $.ajax({
      type: 'POST',
      url: '/write',
      // url: '/upload',
      data: data,
      contentType: false,
      processData: false,
      success: function (response) {
        console.log(response);
        alert("게시글을 작성하였습니다!");
        window.location.href = '/';
      },
    });
  }
}