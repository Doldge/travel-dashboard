define(function(require, exports, module) {
    var React = require('react')
    var marked = require('marked');

    module.exports = React.createClass({
        getDefaultProps: function() {
            return {
                colour : 'blue-grey darken-1',
                text_colour : 'white',
                hoverable : '',
                source : null,
                successFunction : null,
                height : '',
                width : 's12 m6',
                icon : ''
            }
        },
        rawIcon: function() {
            if ( this.props.icon )
                return { __html : '<i style="font-size: 470%; opacity : 0.7" class="material-icons">'+this.props.icon+'</i>' };
            else
                return { __html : ''};
        },
    
        rawTitle: function() {
            return { __html : this.props.title };
        },

        rawContent: function() {
            return { __html: this.props.content };
        },

        componentDidMount: function() {
            if ( this.props.source != null )
            {
                var res = $.get( this.props.source );
                if ( this.props.successFunction )
                    res.success( this.props.successFunction )
                else
                    res.success( function( data ) {
                        this.setState({
                            content : data
                        });
                    });
            }
        },

        render : function() {
            return (
                <div className={"col "+this.props.width}>
                    <div className={"card "+this.props.colour+" "+this.props.text_colour + "-text " + this.props.hoverable + " " + this.props.height}>
                        <div className={"card-content " + this.props.text_colour + "-text"}>
                            <div className="section">
                                <div className="card-icon right" dangerouslySetInnerHTML={this.rawIcon()}/>
                                <span className="card-title" dangerouslySetInnerHTML={ this.rawTitle() }/>
                            </div>
                            <div className="section">
                                <div dangerouslySetInnerHTML={ this.rawContent() }/>
                            </div>
                        </div>
                    </div>
                </div>
            )
        }
    })
});
