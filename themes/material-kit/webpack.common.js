const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const webpack = require('webpack');

module.exports = {
  entry: {
    'main': './src/index.js',
    'index': './src/js/pages/index.js',
    'article': './src/js/pages/article.js'
  },
  output: {
    filename: "js/[name].bundle.js?[hash]",
    path: path.resolve(__dirname, "static")
  },
  externals: {
    jquery: "jQuery"
  },
  module: {
    rules: [
      {
        test: /\.m?js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      },
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
            loader: "css-loader",
          },
          {
            loader: "sass-loader?sourceMap",
            options: {
              sassOptions: {
                indentWidth: 4,
                includePaths: [],
              },
            },
          }
        ]
      },
      {
        test: /\.(woff(2)?|ttf|eot)(\?v=\d+\.\d+\.\d+)?$/,
        use: [
          {
            loader: "file-loader",
            options: {
              name: "[name].[ext]?[hash]",
              outputPath: "fonts/",
              publicPath: "fonts/"
            }
          },
          {
            loader: 'image-webpack-loader',
            options: {},
          },
        ]
      },
      {
        test: /\.(gif|png|jpe?g|svg|cur)$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: "[name].[ext]",
              outputPath: "img/",
              publicPath: "/theme/img/" // Path Pelican publishes the files to
            }
          },
          {
            loader: 'image-webpack-loader',
            options: {}
          }
        ]
      }, // inline base64 URLs for <=30k images, direct URLs for the rest
      {
        // Exposes jQuery for use outside Webpack build
        test: require.resolve('jquery'),
        use: [
          {loader: 'expose-loader', options: 'jQuery'},
          {loader: 'expose-loader', options: '$'}
        ]
      }
    ]
  },
  plugins: [
    new webpack.ProvidePlugin({
      'window.jQuery': 'jquery',
      'window.$': 'jquery',
      'jQuery': 'jquery',
      '$': 'jquery',
      'Popper': ['popper.js', 'default']
    }),
    new MiniCssExtractPlugin({
      filename: "css/[name].bundle.css?[hash]",
      chunkFilename: "css/[name].bundle.css?[hash]"
    }),
  ]
}
;
