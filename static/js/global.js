var CustomHandlers = function() {
  var startdate = null;
  return {
    beenTravellingSuccess : function( data ) {
      console.log( data );
      startdate = new Date( data.startDate * 1000 ).getTime();
      CustomHandlers.timeSinceLeaving();
    },

    timeSinceLeaving : function() {
      setInterval(function() {
        var now = new Date().getTime();
        var delta = (now - startdate) / 1000;
        var days = parseInt(delta / 86400);
        delta = delta % 86400;

        var hours = parseInt(delta / 3600);
        delta = delta % 3600;

        var minutes = parseInt( delta / 60 );
        var seconds = parseInt( delta % 60 );

        $('.time-since-home').find('.countup-timer').html(days + ' Days, ' + hours + ' Hours, ' + minutes + ' Minutes, ' + seconds + ' Seconds');
      }, 1000);
    }
  }
}();


var Functions = function() {
  return {
    format_number : function( n, places )
    {
      if ( isNaN(n) ) return n;
      d = Number(n);
      if ( places != null ) d = parseFloat(d.toFixed(places));
      return d.toLocaleString( window.navigator.userLanguage, { 'style' : 'decimal' });
    }
  }
}();
