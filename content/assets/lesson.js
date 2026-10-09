// 🔊/🐢 링크를 누르면 페이지 안에서 바로 재생하고, '정답과 해설'은 접어서 보여준다.
document$.subscribe(function () {
  var current = null;
  document.querySelectorAll('.md-content a[href$=".mp3"]').forEach(function (a) {
    a.classList.add("audio-btn");
    a.setAttribute("aria-label", "음성 듣기");
    a.addEventListener("click", function (e) {
      e.preventDefault();
      if (current) { current.pause(); }
      current = new Audio(a.href);
      current.play();
    });
  });

  document.querySelectorAll(".md-content h2").forEach(function (h) {
    if (h.textContent.trim().indexOf("정답과 해설") !== 0) return;
    var details = document.createElement("details");
    details.className = "answers";
    details.id = h.id;
    var summary = document.createElement("summary");
    summary.textContent = "정답과 해설 보기";
    details.appendChild(summary);
    var next = h.nextElementSibling;
    while (next && next.tagName !== "H2") {
      var move = next;
      next = next.nextElementSibling;
      details.appendChild(move);
    }
    h.replaceWith(details);
  });
});
