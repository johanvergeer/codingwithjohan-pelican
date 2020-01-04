const merge = require("webpack-merge");
const common = require("./webpack.common.js");
const devServer = require("webpack-dev-server");

module.exports = merge(common, {
    mode: "development",
    watch: true,
    devServer: {
        watchContentBase: true,
        compress: false,
        hot: false,
        liveReload: true,
        writeToDisk: true,
    },
    watchOptions: {
        ignored: ['node_modules', 'static'],
    }
});