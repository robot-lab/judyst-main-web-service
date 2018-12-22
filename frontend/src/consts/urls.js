// var prefix = 'http://127.0.0.1:8000/api';
var prefix = '/api';
export default{
    Search: `${prefix}/search/number_of_links`,
    Document: `${prefix}/search/document`,
    Links: `${prefix}/search/get`,
    Auth_signin: `${prefix}/user/login`,
    Auth_signup: `${prefix}/user/register`,
    Auth_signout: `${prefix}/user/logout`,

}