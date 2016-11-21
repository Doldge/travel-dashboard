requirejs(['jquery', 'react-dom', 'react'], function(jQuery, ReactDOM, React) {
  //Load the Index Content.
  if ( window.location.pathname == '/' )
  {
    requirejs(['jsx!components/card', 'jsx!components/table', '//maps.googleapis.com/maps/api/js?key='+Public.mapKey, 'jsx!components/map'], function( Card, Table, google, Map ) {
      $(function() {
        var distFromHome =  {
          'icon' : 'navigation',
          'title' : 'Distance From Home',
          'content' : '<span id="distFromHome"></span>',
          'hoverable' : 'hoverable',
          'colour' : 'teal lighten-3',
          'source' : '/myaccount/distancefromhome/'+Public.id+'/',
          'width' : 's12 m12 l6',
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
          'width' : 's12 m12 l6',
          'source' : '/myaccount/totaldistance/'+Public.id+'/',
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
          'source' : '/myaccount/timesincedeparture/'+Public.id+'/',
          'successFunction' : CustomHandlers.beenTravellingSuccess,
          'width' : 's12 m12 l6',
        };

        var friendCount = {
          'title' : 'Friends Made Since Leaving',
          //'content' : '<p>Callum has made 12 friends since leaving home</p>',
          'content' : '<span id="friendCount"></span>',
          'hoverable' : 'hoverable',
          'colour' : 'blue',
          'icon' : 'people',
          'source' : '/myaccount/friends/'+Public.id+'/',
          'width' : 's12 m12 l6',
          'successFunction' : function( data )
          {
            console.log( data );
            $('#friendCount').html('<p>'+data.name+' has made '+data.friends+' friends since leaving home</p>');
          }
        };

        var travelTable = {
          'title' : 'Travel Locations',
          'source' : 'myaccount/locations/table/'+Public.id+'/'
        }

        var travelMap = {
          'source' : 'myaccount/locations/'+Public.id+'/'
        }

        ReactDOM.render( React.createElement( Card, distFromHome ), $('.distance-from-home')[0] );
        ReactDOM.render( React.createElement( Card, distTravelled ), $('.total-distance-travelled')[0] );
        ReactDOM.render( React.createElement( Card, beenTravelling ), $('.time-since-home')[0] );
        ReactDOM.render( React.createElement( Card, friendCount ), $('.friend-count')[0] );
        ReactDOM.render( React.createElement( Table, travelTable ), $('.locations-visited-list')[0] );
        ReactDOM.render( React.createElement( Map, travelMap ), $('.locations-visited-map')[0] );
        //ReactDOM.render( React.createElement( Map, travelMap), $('.locations-visited-list')[0] );
      });
    });
  }
});
