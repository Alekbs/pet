  var button = document.querySelector("button");
  button.addEventListener("click", function() {
    console.log("Кнопка нажата.");
  });
    var eventSource = new EventSource("/listen")

    eventSource.addEventListener("message", function(e) {
      console.log(e.data)
    }, false)

    eventSource.addEventListener("online", function(e) {
      // console.log(e.data.color)
      data = JSON.parse(e.data)
      document.querySelector("#text").innerText = data.text
    }, true)
