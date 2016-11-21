define(function(require, exports, module) {
    var React = require('react');
    var Loader = require('jsx!components/loader');

    module.exports = React.createClass({
        getDefaultProps: function() {
            return {
                source : null,
                initialZoom: 2,
                mapCenterLat: 43.6425569,
                mapCenterLng: 0,
                mapTypeId: google.maps.MapTypeId.SATELLITE
            }
        },
        
        getInitialState: function() {
            return {
                locations : [],
            }
        },
    
        rawTitle: function() {
            return { __html : this.props.title };
        },

        rawContent: function() {
            return { __html: this.props.content };
        },

        componentDidMount: function() {
            var mapOptions = {
                center: this.mapCenterLatLng(),
                zoom: this.props.initialZoom
            };
            console.log(this.getDOMNode());
            map = new google.maps.Map(this.getDOMNode(), mapOptions);
            var marker = new google.maps.Marker({position: this.mapCenterLatLng(), title: 'Hi', map: map});
            this.setState({map: map});
            
            if ( this.props.source != null )
            {
                var self = this;
                $.get( this.props.source, function( data ) {
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
                        marker.setMap(self.state.map);
                    }
                    self.setState({
                        locations : locations
                    });
                }.bind(this) );
            }
        },

        mapCenterLatLng: function () {
            var props = this.props;
            return new google.maps.LatLng(props.mapCenterLat, props.mapCenterLng);
        },

        render : function() {
            return (
                <div className='map-gic' style={{'width' : '80%', 'height' : '700px'}}></div>
            )
        }
    })
});
