module.exports = {
    baseUrl: process.env.NODE_ENV === 'production'
      ? '/static/'
      : '/',
    outputDir: 'dist/static'
  }