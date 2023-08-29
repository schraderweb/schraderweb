fetch("./int-page-nav.html")
  .then(response => {
    return response.text()
  })
  .then(data => {
    document.querySelector("body").innerHTML += data;
  });

fetch("./int-page-footer.html")
  .then(response => {
    return response.text()
  })
  .then(data => {
    document.querySelector("body").innerHTML += data;
  });


