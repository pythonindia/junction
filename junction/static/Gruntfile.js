/*global module:false*/
module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    // Task configuration.
     watch: {
      less: {
        files: [ 'less/**/*.less' ],
        tasks: [ 'less' ]
      }
    },
    less: {
      compile: {
        files: {
          './css/app.css': './less/app.less'
        }
      }
    }
  });

  // These plugins provide necessary tasks.
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-watch');

  // Default task.
  grunt.registerTask('default', ['less', 'watch']);

};
