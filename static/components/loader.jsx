define(function(require, exports, module) {
    var React = require('react')

    module.exports = React.createClass({
        getDefaultProps: function() {
            return {
                visible : 'hidden'
            }
        },

        render : function() {
            return (
                <div className="preloader-wrapper big active" style={{"visibility" : this.props.visible}}>
                    <div className="spinner-layer spinner-blue-only" >
                        <div className="circle-clipper left">
                            <div className="circle"></div>
                        </div><div className="gap-patch">
                            <div className="circle"></div>
                        </div><div className="circle-clipper right">
                            <div className="circle"></div>
                        </div>
                    </div>
                </div>
            )
        }
    })
});
