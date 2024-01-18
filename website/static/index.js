
function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ codeId: codeId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }