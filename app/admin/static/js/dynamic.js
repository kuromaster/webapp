function handlerBtnEditRecord(e) {
  e.preventDefault();
  e.stopPropagation();

  var url = $(this).data('url');
  // var id = $('#modalAddRecord input').attr('id');


  $.get(url, function (data) {
    console.log('GET data status: ' + data.status)

    $('#modalAddRecord h5').text('Редактирование записи');
    $('#modalAddRecord #btn-modal-post').text('Изменить');
    $('#modalAddRecord #btn-modal-post').removeClass("btn-danger").addClass("btn-success");
    $('#modalAddRecord #btn-modal-post').prop('type','button');


    $('#modalAddRecord input.form-control ').each(function(){
      var id = $(this).attr('id');
      $('#modalAddRecord .modal-content #'+id).val(data[id]);

    });

    $('#modalAddRecord .modal-content #body').summernote('code', data.body);

    $('#modalAddRecord').modal('show');

    $('#btn-modal-post').click(function (event) {
      event.preventDefault();
      event.stopPropagation();
      var data = $('#modal-form-Post').serialize();

      $.post(url, data = $('#modal-form-Post').serialize(), function (data) {
          console.log('POST status from python: ' + data.status);
          if (data.status == 'ok'){
            $('#modalAddRecord').modal('hide');
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


function handerBtnAddRecord(e) {
  e.preventDefault();

  $('#modalAddRecord input.form-control ').each(function(){
    var id = $(this).attr('id');
    $('#modalAddRecord .modal-content #'+id).val('');
  });
  $('#modalAddRecord .modal-content #body').summernote('code', '');

  $('#modalAddRecord h5').text('Новый пост');
  $('#modalAddRecord #btn-modal-post').text('Создать');
  $('#modalAddRecord #btn-modal-post').prop('type','submit');
  $('#modalAddRecord #btn-modal-post').removeClass("btn-danger").addClass("btn-success");


}


function handlerBtnRemoveRecord(e) {
  e.preventDefault();
  e.stopPropagation();
  var url = $(this).data('url');
  // var id = $(this).data('pk');

  // console.log('url: ' + url);
  $.get(url, function (data) {
    console.log('GET data status: ' + data.status);
    // console.log('GET data: ' + data);
    $('#modalspanDelete').text('id = ' + data.id + ' ?');
    $('#modalDeleteRow').modal('show');

    $('#btnDelteYes').click(function (event) {
      event.preventDefault();
      event.stopPropagation();
      $.post(url, {'id': data.id}, function (
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


function handlerBtnGlobalRemoveRecord(e) {
  e.preventDefault();
  e.stopPropagation();
  var url = $(this).data('url');
  var data_arr = [];

  // var id = $(this).data('pk');

  // console.log('url: ' + url);

  $.get(url, function (data) {
    console.log('GET data status: ' + data.status);
    // console.log('GET data: ' + data);
    $('#modalspanDelete').text('');
    $('#modalDeleteRow').modal('show');

    $('#btnDelteYes').click(function (event) {
      event.preventDefault();
      event.stopPropagation();


      $("input.checkboxRows").each(function(){
        if ($(this).is(":checked")) {
          data_arr.push($(this).attr("data-pk"));
        }
      });
      $('#modalDeleteRow').data('id', data_arr);
      // data_arr = {"id": data_arr};
      // console.log(data_arr);

      $.post(url, data = {"id": $('#modalDeleteRow').data('id')}, function (
        data) {
          console.log(data);
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
          console.log('POST edit: js error');
        })
        .always(function (){
          $('#btnDelteYes').off("click");

        });

    });
 });
}

function itemCheckboxEvent() {
  var checkbox = $('table tbody input[type="checkbox"]');
  $("#selectAll").click(function(){
    if(this.checked){
      checkbox.each(function(){
        this.checked = true;
      });
    } else{
      checkbox.each(function(){
        this.checked = false;
      });
    }
  });
  checkbox.click(function() {
    if(!this.checked){
      $("#selectAll").prop("checked", false);
    }
  });
}
