document.addEventListener("htmx:confirm", (e) => {
  if (!e.target.classList.contains("btn-delete")) if (!e.target.classList.contains("btn-delete-task")) return;

  e.preventDefault()
  Swal.fire({
    title: "Remover?",
    iconColor: "#dc143c",
    text: `${e.detail.question}`,
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#dc143c",
    confirmButtonText: "Remover",
    cancelButtonText: "Cancelar",
  }).then(result => {
    if (result.isConfirmed) {
      e.detail.issueRequest(true);
    }
  })
});