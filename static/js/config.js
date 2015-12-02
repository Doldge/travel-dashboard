requirejs.config({
  baseUrl: '../static',
  paths : {
    jquery : 'vendors/jquery/dist/jquery',
    jsx : 'vendors/jsx-requirejs-plugin/js/jsx',
    JSXTransformer : 'vendors/jsx-requirejs-plugin/js/JSXTransformer',
    text : 'vendors/requirejs-text/text',
    react : 'vendors/react/react-with-addons',
    'react-dom' : 'vendors/react/react-dom',
    'mdl' : 'vendors/material-design-lite/material.min',
    'materialize' : 'vendors/Materialize/dist/js/materialize',
    'marked' : 'vendors/marked/marked.min'
  },
  jsx : {
    fileExtension : '.jsx',
  }
});
