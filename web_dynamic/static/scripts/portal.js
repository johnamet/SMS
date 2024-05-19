  export function portal (path) {
    window.location.host = '127.0.0.1';
    window.location.port = 8081;
    window.location.pathname = '/' + path;
  }

  export function service(path){
    return 'http://127.0.0.1:8080/services/v1/'+path
  }