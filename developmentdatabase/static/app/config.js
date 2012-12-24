require.config({
  // deps: [
  //   window.location.pathname === '/_test' ? 'test/config' : 'main'
  // ],
  deps: [
    'main'
  ],
  paths: {
    lodash: '/static/lib/lodash/lodash',
    backbone: '/static/lib/backbone/backbone',
    jquery: '/static/lib/jquery/jquery-1.8.3'
  }//,
  // shim: {
  //   'socketio': {
  //     exports: 'io'
  //   },
  //   'underscore': {
  //     exports: '_'
  //   },
  //   'backbone': {
  //     exports: 'Backbone',
  //     deps: [ 'jquery', 'underscore' ]
  //   }
  // }
});