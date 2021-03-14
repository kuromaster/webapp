function handlerBtnEditPost(e) {
  e.preventDefault();
  e.stopPropagation();
  var url = $(this).data('slug');
  // console.log('url: ' + url);
  $.get(url, function (data) {
    console.log('GET data status: ' + data.status)
    // console.log('data title: ' + data.title)
    // console.log('data body: ' + data.body)
    $('#modalCreatePost h5').text('Редактирование поста');
    $('#modalCreatePost #btn-modal-post').text('Изменить');
    $('#modalCreatePost #btn-modal-post').removeClass("btn-danger").addClass("btn-success");
    $('#modalCreatePost #btn-modal-post').prop('type','button');
    $('#modalCreatePost .modal-content #title').val(data.title);
    $('#modalCreatePost .modal-content #body').summernote('code', data.body);
    $('#modalCreatePost').modal('show');

    $('#btn-modal-post').click(function (event) {
      event.preventDefault();
      event.stopPropagation();
      $.post(url, data = $('#modal-form-Post').serialize(), function (
        data) {
          console.log(data.status);
          if (data.status == 'ok'){
            $('#modalCreatePost').modal('hide');
            location.reload();
          }
        })
        .done(function(){
          console.log('POST data status: success');

        })
        .fail(function(){
          console.console.log('POST edit: js error');
        })
        .always(function (){
          $('#btn-modal-post').off("click");

        });

    });
 });
}

function handerBtnCreatePost(e) {
  e.preventDefault();

  $('#modalCreatePost h5').text('Новый пост');
  $('#modalCreatePost #btn-modal-post').text('Создать');
  $('#modalCreatePost #btn-modal-post').prop('type','submit');
  $('#modalCreatePost #btn-modal-post').removeClass("btn-danger").addClass("btn-success");
  $('#modalCreatePost .modal-content #title').val('');
  $('#modalCreatePost .modal-content #body').summernote('code', '');

}

function handlerBtnRemovePost(e) {
  e.preventDefault();
  e.stopPropagation();
  var url = $(this).data('slug');
  // var id = $(this).data('pk');

  // console.log('url: ' + url);
  $.get(url, function (data) {
    console.log('GET data status: ' + data.status);
    console.log('GET data: ' + data);
    $('#modalspanDelete').text(data.title + ' ?');
    $('#modalDeletePost').modal('show');

    $('#btnDelteYes').click(function (event) {
      event.preventDefault();
      event.stopPropagation();
      $.post(url, {'id': data.id, 'title': data.title}, function (
        data) {
          console.log(data.status);
          if (data.status == 'ok'){
            console.log('data id: ' + data.id)
            $('#modalCreatePost').modal('hide');
            location.reload();
          }
        })
        .done(function(){
          console.log('POST data status: success');

        })
        .fail(function(){
          console.console.log('POST edit: js error');
        })
        .always(function (){
          $('#btnDelteYes').off("click");

        });

    });
 });
}
