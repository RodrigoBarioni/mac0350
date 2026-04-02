document.body.addEventListener('htmx:afterSwap', function (evt) {
  MicroModal.init({
    awaitCloseAnimation: true
  });
});