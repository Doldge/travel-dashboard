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

requirejs(['jquery', 'react-dom', 'react'], function(jQuery, ReactDOM, React) {
  //Load the Index Content.
  if ( window.location.pathname == '/' )
  {
    requirejs(['jsx!components/card'], function( Card ) {
      $(function() {
        var distFromHome =  {
          'icon' : 'navigation',
          'title' : 'Distance From Home', 
          'content' : '<p>Currently <span class="distance">5,000</span> <span class="distance-unit">miles</span> from home</p>',
          'hoverable' : 'hoverable',
          'colour' : 'teal lighten-3' 
        };

        var distTravelled = {
          'icon' : 'motorcycle',
          'title' : 'Total Distance Travelled',
          'content' : '<p>Travelled a total of <span class="distance">8,000</span> <span class="distance-unit">miles</span> since leaving home.',
          'hoverable' : 'hoverable',
          'width' : 's12 m6'
        };
    
        var beenTravelling = {
          'icon' : 'home',
          'title' : 'Time Since Departure',
          'content' : '<span class="countup-timer"></span>',
          'hoverable' : 'hoverable',
          'colour' : 'amber darken-3',
          'source' : '/timeSinceHome/',
          'successFunction' : CustomHandlers.beenTravellingSuccess,
          'width' : 's12 m6'
        }; 

      var friendCount = {
        'title' : 'Friends Made Since Leaving',
        'content' : '<p>Callum has made 12 friends since leaving home</p>',
        'hoverable' : 'hoverable',
        'colour' : 'blue',
      };

        ReactDOM.render( React.createElement( Card, distFromHome ), $('.distance-from-home')[0] );
        ReactDOM.render( React.createElement( Card, distTravelled ), $('.total-distance-travelled')[0] );
        ReactDOM.render( React.createElement( Card, beenTravelling ), $('.time-since-home')[0] );
        ReactDOM.render( React.createElement( Card, friendCount ), $('.friend-count')[0] );
      });
    });
  }
});
