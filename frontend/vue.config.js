module.exports = {
    baseUrl: process.env.NODE_ENV === 'production'
      ? '/static/'
      : '/',
    outputDir: 'dist/static',
    configureWebpack: {
      resolve: {
        alias: {
          vue$: "vue/dist/vue.common",
        },
      },
    },
  }