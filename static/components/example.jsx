define(function(require, exports, module) {
    var React = require('react')
    var ReactDOM = require('react-dom')
    var jquery = require('jquery')
    
    module.exports = React.createClass({

        getInitialState : function() {
            return {
                colour_1 : 'red',
                colour_2 : 'blue',
                data : '<g id="Gridlines">' +
                        '<line fill="#888888" stroke="#888888" stroke-miterlimit="10" x1="0" y1="27.3" x2="468.3" y2="27.3">' +
                        '<line fill="#888888" stroke="#888888" stroke-miterlimit="10" x1="0" y1="66.7" x2="468.3" y2="66.7">' +
                        '<line fill="#888888" stroke="#888888" stroke-miterlimit="10" x1="0" y1="105.3" x2="468.3" y2="105.3">' +
                        '<line fill="#888888" stroke="#888888" stroke-miterlimit="10" x1="0" y1="144.7" x2="468.3" y2="144.7">' +
                        '<line fill="#888888" stroke="#888888" stroke-miterlimit="10" x1="0" y1="184.3" x2="468.3" y2="184.3">' +
                    '</g>' +
                    '<g id="Numbers">' +
                        '<text transform="matrix(1 0 0 1 485 29.3333)" fill="#888888" font-family="\'Roboto\'" font-size="9">500</text>' +
                        '<text transform="matrix(1 0 0 1 485 69)" fill="#888888" font-family="\'Roboto\'" font-size="9">400</text>' +
                        '<text transform="matrix(1 0 0 1 485 109.3333)" fill="#888888" font-family="\'Roboto\'" font-size="9">300</text>' +
                        '<text transform="matrix(1 0 0 1 485 149)" fill="#888888" font-family="\'Roboto\'" font-size="9">200</text>' +
                        '<text transform="matrix(1 0 0 1 485 188.3333)" fill="#888888" font-family="\'Roboto\'" font-size="9">100</text>' +
                        '<text transform="matrix(1 0 0 1 0 249.0003)" fill="#888888" font-family="\'Roboto\'" font-size="9">1</text>' +
                        '<text transform="matrix(1 0 0 1 78 249.0003)" fill="#888888" font-family="\'Roboto\'" font-size="9">2</text>' +
                        '<text transform="matrix(1 0 0 1 154.6667 249.0003)" fill="#888888" font-family="\'Roboto\'" font-size="9">3</text>' +
                        '<text transform="matrix(1 0 0 1 232.1667 249.0003)" fill="#888888" font-family="\'Roboto\'" font-size="9">4</text>' +
                        '<text transform="matrix(1 0 0 1 309 249.0003)" fill="#888888" font-family="\'Roboto\'" font-size="9">5</text>' +
                        '<text transform="matrix(1 0 0 1 386.6667 249.0003)" fill="#888888" font-family="\'Roboto\'" font-size="9">6</text>' +
                        '<text transform="matrix(1 0 0 1 464.3333 249.0003)" fill="#888888" font-family="\'Roboto\'" font-size="9">7</text>' +
                    '</g>' +
                    '<g id="Layer_5">' +
                        '<polygon opacity="0.36" stroke-miterlimit="10" points="0,223.3 48,138.5 154.7,169 211,88.5 294.5,80.5 380,165.2 437,75.5 469.5,223.3   ">' +
                    '</g>' +
                    '<g id="Layer_4">' +
                        '<polygon stroke-miterlimit="10" points="469.3,222.7 1,222.7 48.7,166.7 155.7,188.3 212,132.7 296.7,128 380.7,184.3 436.7,125   ">' +
                    '</g>'
            }
        },
        componentDidMount: function() {
            $.get(this.props.source, function( result ) {
                if ( this.isMounted() ) {
                    const element = ReactDOM.findDOMNode(this);
                    jquery(element).find('.svg-1').attr('fill', result.colour_1);
                    jquery(element).find('.svg-2').attr('fill', result.colour_2);
                    jquery(element).find('.svg-1').append(this.state.data);
                    jquery(element).find('.svg-2').append(this.state.data);
                    this.setState({
                        colour_1 : result.colour_1,
                        colour_2 : result.colour_2
                    });
                }
            }.bind(this));
        },
        render: function() {
            return (
                <div class="demo-graphs mdl-shadow--2dp mdl-color--white mdl-cell mdl-cell--8-col">
                    <svg viewBox="0 0 500 250" class="demo-graph svg-1">
                    </svg>
                    <svg viewBox="0 0 500 250" class="demo-graph svg-2">
                    </svg>
                </div>
            )
        }
    })
});
