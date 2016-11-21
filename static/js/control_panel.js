requirejs(['jquery', 'react-dom', 'react', 'materialize'], function(jQuery, ReactDOM, React, Materialize) {
  requirejs(['jsx!components/card'], function( Card ) {
      $(function() {
        var distFromHome =  {
          'icon' : 'navigation',
          'title' : 'Distance From Home',
          'content' : '<span id="distFromHome"></span>',
          'hoverable' : 'hoverable',
          'colour' : 'teal lighten-3',
          'source' : '/myaccount/distancefromhome/',
          'successFunction' : function( data )
            {
              console.log(data);
              $('#distFromHome').html('<p>Currently <span class="distance">'+Functions.format_number(data.distance/1000,0)+'</span> <span class="distance-unit">KM</span> from home</p>');
            }
        };

        var distTravelled = {
          'icon' : 'motorcycle',
          'title' : 'Total Distance Travelled',
          'content' : '<span id="distTravelled"></span>',
          'hoverable' : 'hoverable',
          'width' : 's12 m6',
          'source' : '/myaccount/totaldistance/',
          'successFunction' : function( data )
            {
              console.log(data);
              $('#distTravelled').html('<p>Travelled a total of <span class="distance">'+Functions.format_number(data.distance/1000,0)+'</span> <span class="distance-unit">KM</span> since leaving home.') 
            }
        };

        var beenTravelling = {
          'icon' : 'home',
          'title' : 'Time Since Departure',
          'content' : '<span class="countup-timer"></span>',
          'hoverable' : 'hoverable',
          'colour' : 'amber darken-3',
          'source' : '/myaccount/timesincedeparture/',
          'successFunction' : CustomHandlers.beenTravellingSuccess,
          'width' : 's12 m6'
        };

        var friendCount = {
          'title' : 'Friends Made Since Leaving',
          //'content' : '<p>Callum has made 12 friends since leaving home</p>',
          'content' : '<span id="friendCount"></span>',
          'hoverable' : 'hoverable',
          'colour' : 'blue',
          'icon' : 'people',
          'source' : '/myaccount/friends/',
          'successFunction' : function( data )
          {
            console.log( data );
            $('#friendCount').html('<p>'+data.name+' has made '+data.friends+' friends since leaving home</p>'); 
          }
        };

        ReactDOM.render( React.createElement( Card, distFromHome ), $('.distance-from-home')[0] );
        ReactDOM.render( React.createElement( Card, distTravelled ), $('.total-distance-travelled')[0] );
        ReactDOM.render( React.createElement( Card, beenTravelling ), $('.time-since-home')[0] );
        ReactDOM.render( React.createElement( Card, friendCount ), $('.friend-count')[0] );
      });
  });

  $('.facebook_form').on('submit',function( e ) {
    if ( $('.facebook_form').find('input[name="token"]').length == 0 )
    {
      e.preventDefault();
      myFacebookLogin();
      return false;
    }
  });

  $('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 15 // Creates a dropdown of 15 years to control year
  });

  resp = jQuery.get('/myaccount/locations/');
  resp.success(function(data) {
    console.log( data );
    var locations = [];
    for ( var i = 0; i < data.locations.length; i ++ )
    {
      locations.push(data.locations[i]);
    }
    for (var i = 0; i < locations.length; i++)
    {
      var marker = new google.maps.Marker({
        position : { 'lat' : locations[i]['lat'], 'lng' : locations[i]['lng'] },
        title : locations[i]['name']
      });
      marker.setMap(window.map);
    };
  });
});

