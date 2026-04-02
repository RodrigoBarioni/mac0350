tippy('.btn-add-block', {
  arrow: false,
  content: 'Novo bloco <p class="keyboardKey">CTRL+ALT+N</p>',
  allowHTML: true,
});

tippy.delegate('.blocks', {
  target: '.btn-delete',
  content: 'Remover bloco de tarefas',
  arrow: false,
});

tippy.delegate('.blocks', {
  target: '.btn-edit',
  content: 'Editar informações do bloco',
  arrow: false,
});

tippy.delegate('.right', {
  target: '.btn-edit-title',
  content: 'Editar informações do bloco',
  arrow: false,
});

tippy.delegate('.right', {
  target: '.btn-new-task',
  arrow: false,
  content: 'Nova tarefa <p class="keyboardKey">SHIFT+ALT+N</p>',
  allowHTML: true,
});

tippy.delegate('.right', {
  target: '.btn-complete-task',
  content: 'Concluir tarefa',
  arrow: false,
});

tippy.delegate('.right', {
  target: '.btn-edit-task',
  content: 'Editar tarefa',
  arrow: false,
});

tippy.delegate('.right', {
  target: '.btn-delete-task',
  content: 'Remover tarefa',
  arrow: false,
});

tippy.delegate('.right', {
  target: '.btn-undo-complete',
  content: 'Desmarcar tarefa como concluída',
  arrow: false,
});

tippy('[data-tippy-content]', {
  arrow: false,
});