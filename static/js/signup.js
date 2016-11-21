requirejs(['jquery', 'react-dom', 'react', 'materialize'], function(jQuery, ReactDOM, React, Materialize) {
  //Load the Index Content.
  $('.fix-me').on('click', function() {
    $(this).find('input')[0].checked = !$(this).find('input')[0].checked;
  });

  $('form').on('submit', function( e ) {
    if ( ! $('input[name="t_and_c"]')[0].checked ){
      e.preventDefault();
      $('#plz_tc').openModal();
      return false;
    }
    if ( $('form').find('input[name="token"]').length == 0 ) {
      e.preventDefault();
      $('#plz_fb').openModal();
      return false;
    }
  });

  $('button[name="facebook"]').on('click',function( e ) {
    myFacebookLogin();
  });
});
