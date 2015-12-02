({
  preserveLicenseComments: true,
  optimize: "uglify2",
  uglify2: {
    output: {
      beautify: false,
      comments: false
    },
    compress: {
      drop_console: true
    }
  },
  paths : {
    jquery : "empty:",
    jsx : "vendors/jsx-requiresjs-plugin/js/jsx",
    JSXTransformer : "vendors/jsx-requiresjs-plugin/js/JSXTransformer",
    text : "vendors/requirejs-text/text",
    react : "vendors/react/react-with-addons.min",
    "react-dom" : "vendors/react/react-dom.min",
    "material" : "vendors/material-design-lite/material.min",
    'marked' : 'vendors/marked/marked.min'
  },
  jsx : {
    fileExtension : ".jsx"
  },
  stubModules : [ "jsx", "JSXTransformer", "text" ]
})
