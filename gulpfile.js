// gulp
var gulp = require('gulp');

// plugins
var connect = require('gulp-connect');
var jshint = require('gulp-jshint');
var uglify = require('gulp-uglify');
var minifyCSS = require('gulp-minify-css');
var clean = require('gulp-clean');
var browserify = require('gulp-browserify');
var concat = require('gulp-concat');
var runSequence = require('run-sequence');

// tasks
gulp.task('lint', function() {
  gulp.src(['./waitress/client/app/**/*.js', '!./waitress/client/app/lib/**'])
    .pipe(jshint())
    .pipe(jshint.reporter('default'))
    .pipe(jshint.reporter('fail'));
});
gulp.task('clean', function() {
    gulp.src('./waitress/client/dist/*')
      .pipe(clean({force: true}));
    gulp.src('./waitress/client/app/js/bundled.js')
      .pipe(clean({force: true}));
});
gulp.task('minify-css', function() {
  var opts = {comments:true,spare:true};
  gulp.src(['./waitress/client/app/**/*.css', '!./waitress/client/app/lib/**'])
    .pipe(minifyCSS(opts))
    .pipe(gulp.dest('./waitress/client/dist/'));
});
gulp.task('minify-js', function() {
  gulp.src(['./waitress/client/app/**/*.js', '!./waitress/client/app/lib/**'])
    .pipe(uglify({
      // inSourceMap:
      // outSourceMap: "waitress/client/app.js.map"
    }))
    .pipe(gulp.dest('./waitress/client/dist/'));
});
gulp.task('copy-bower-components', function () {
  gulp.src('./waitress/client/app/lib/**')
    .pipe(gulp.dest('waitress/client/dist/lib'));
});
gulp.task('copy-html-files', function () {
  gulp.src('./waitress/client/app/**/*.html')
    .pipe(gulp.dest('waitress/client/dist/'));
});
gulp.task('connect', function () {
  connect.server({
    root: 'waitress/client/app/',
    port: 8888
  });
});
gulp.task('connectDist', function () {
  connect.server({
    root: 'waitress/client/dist/',
    port: 9999
  });
});
gulp.task('browserify', function() {
  gulp.src(['waitress/client/app/js/main.js'])
  .pipe(browserify({
    insertGlobals: true,
    debug: true
  }))
  .pipe(concat('bundled.js'))
  .pipe(gulp.dest('./waitress/client/app/js'));
});
gulp.task('browserifyDist', function() {
  gulp.src(['waitress/client/app/js/main.js'])
  .pipe(browserify({
    insertGlobals: true,
    debug: true
  }))
  .pipe(concat('bundled.js'))
  .pipe(gulp.dest('./waitress/client/dist/js'));
});


// // *** default task *** //
// gulp.task('default',
//   ['lint', 'browserify', 'connect']
// );
// // *** build task *** //
// gulp.task('build',
//   ['lint', 'minify-css', 'browserifyDist', 'copy-html-files', 'copy-bower-components', 'connectDist']
// );

// *** default task *** //
gulp.task('default', function() {
  runSequence(
    ['clean'],
    ['lint', 'browserify', 'connect']
  );
});
// *** build task *** //
gulp.task('build', function() {
  runSequence(
    ['clean'],
    ['lint', 'minify-css', 'browserifyDist', 'copy-html-files', 'copy-bower-components', 'connectDist']
  );
});
