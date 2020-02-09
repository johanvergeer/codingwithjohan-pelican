const merge = require("webpack-merge");
const common = require("./webpack.common.js");
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const PurgecssPlugin = require('purgecss-webpack-plugin');
const glob = require('glob-all');

module.exports = merge(common, {
  mode: "production",
  optimization: {
    minimizer: [new UglifyJsPlugin({
      uglifyOptions: {
        output: {
          comments: false,
        },
      },
    })],
  },
  plugins: [
    new PurgecssPlugin({
      paths: glob.sync([
        'templates/**'
      ], {nodir: true}),
      whitelist: [
        'blockquote', 'table', 'title', 'checklist', 'code',
        // Code highlight
        'highlight', 'hll', 'c', 'err', 'k', 'o', 'ch', 'cm', 'cp', 'cpf', 'c1', 'cs', 'gd', 'ge', 'gr', 'gh', 'gi',
        'go', 'gp', 'gs', 'gu', 'gt', 'kc', 'kd', 'kn', 'kp', 'kr', 'kt', 'm', 's', 'na', 'nb', 'nc', 'no', 'nd',
        'ni', 'ne', 'nf', 'nl', 'nn', 'nt', 'nv', 'ow', 'w', 'mb', 'mf', 'mh', 'mi', 'mo', 'sa', 'sb', 'sc', 'dl',
        'sd', 's2', 'se', 'sh', 'si', 'sx', 'sr', 's1', 'ss', 'bp', 'fm', 'vc', 'vg', 'vi', 'vm', 'il', 'n',
        // Cards
        'mk-card', 'card-header', 'card-header-primary',
        'card-header-success', 'card-header-warning', 'card-header-info', 'card-header-danger', 'card-header-rose',
        'card-header-icon', 'card-icon', 'card-body',
        'material-icons',
        // Table of contents
        'toc',
        // Procon
        'procon', 'pro', 'con'
      ]
    })
  ]
});
