async function press(id) {
  $(".btn-primary").removeClass("btn-primary");
  $(".btn").addClass("btn-light");
  var name = $("#namebox").val();
  var uni = $("#unibox").val();
  var op = 0;
  var ans;
  var ele = document.getElementsByName("sentiment_choice");
  for (i = 0; i < ele.length; i++) {
    if (ele[i].checked) {
      op = ele[i].value;
    }
  }

  if (name.length == 0) {
    alert("The name was not provided. Please try again!");
  } else if (uni.length == 0) {
    alert("The university was not provided. Please try again!");
  } else if (op == 0) {
    alert("The method was not selected. Please try again!");
  } else {
    var inp = { name: name, uni: uni, op: op };

    document.getElementById("loading").innerHTML = "Loading...";
    await $.ajax({
      url: "/test",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(inp),
    }).then((res) => {
      ans = res["answer"];
    });
    document.getElementById("loading").innerHTML = ans;
  }
  $(".btn").removeClass("btn-light");
  $(".btn").addClass("btn-primary");
}
