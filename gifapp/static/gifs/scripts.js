function saveGif(gifUrl){
  csrf_token = Cookies.get('csrftoken');
  xhr = new XMLHttpRequest();
  xhr.open('POST', '/gifs/new/'+ encodeURI(gifUrl));
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.setRequestHeader('X-CSRFToken', csrf_token)
  xhr.onload = function() {
      if (Math.floor(xhr.status / 100) != 2){
          alert('Sorry, gif not saved.  Returned status of ' + xhr.status);
      }
      document.getElementById(gifUrl).innerHTML = "Saved";
  };
  xhr.send()
}
