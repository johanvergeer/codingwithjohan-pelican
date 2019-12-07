const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const webpack = require('webpack');

module.exports = {
    entry: './src/index.js',
    output: {
        filename: "js/[name].js?[hash]",
        path: path.resolve(__dirname, "static")
    },
    externals: {
        jquery: "jQuery"
    },
    module: {
        rules: [
            {
                test: /\.scss$/,
                use: [
                    {
                        loader: MiniCssExtractPlugin.loader,
                        options: {
                            hmr: false,
                            reloadAll: true
                        }
                    },
                    {
                        loader: "css-loader"
                    },
                    {
                        loader: "sass-loader",
                        options: {
                            sassOptions: {
                                indentWidth: 4,
                                includePaths: [
                                    'node_modules/material-kit/assets/scss',
                                ],
                            },
                        },
                    }
                ]
            },
            {
                test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
                use: [
                    {
                        loader: "file-loader",
                        options: {
                            name: "[name].[ext]?[hash]",
                            outputPath: "css/fonts/",
                            publicPath: "fonts/"
                        }
                    }
                ]
            },
            {
                // Exposes jQuery for use outside Webpack build
                test: require.resolve('jquery'),
                use: [
                    {loader: 'expose-loader', options: 'jQuery'},
                    {loader: 'expose-loader', options: '$'}
                ]
            },
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: "css/[name].css?[hash]",
            chunkFilename: "css/[name].css?[hash]"
        }),
        new webpack.ProvidePlugin({
            'window.jQuery': 'jquery',
            'window.$': 'jquery',
            'jQuery': 'jquery',
            '$': 'jquery',
            'Popper': ['popper.js', 'default']
        }),
    ]
}
;