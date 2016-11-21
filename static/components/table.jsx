define(function(require, exports, module) {
    var React = require('react');
    var Loader = require('jsx!components/loader');

    module.exports = React.createClass({
        getDefaultProps: function() {
            return {
                colour : 'blue-grey darken-1',
                text_colour : 'white',
                hoverable : '',
                source : null,
                height : '',
                width : 's12 m6',
                icon : '',
                visible : '',
            }
        },
        
        getInitialState: function() {
            return {
                headers : [],
                rows : [],
                successFunction : null,
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
                var t = this;
                $.get( this.props.source, function( data ) {
                    var headers = [];
                    var rows = [];
                    for (var i =0; i <data.headers.length; i++)
                    {
                        headers.push(<td>{data.headers[i]}</td>);
                    } 
                    for (var i=0; i < data.rows.length; i++)
                    {
                        var k = data.rows[i];
                        var row = [];
                        for(var j=0;j<k.length;j++)
                        {
                            row.push(<td>{k[j]}</td>);
                        }
                        rows.push(<tr>{row}</tr>);
                    }
                        this.setState({
                            headers : headers,
                            rows : rows
                        });
                    }.bind(this)
                );
            }
        },

        render : function() {
            return (
                <div className={"col "+this.props.width}>
                    <table className={"bordered"}>
                        <thead>
                          <tr>
                            {this.state.headers}
                          </tr>
                        </thead>
                        <tbody>
                            {this.state.rows}
                        </tbody>
                    </table>
                </div>
            )
        }
    })
});
