const btnsActualizar = document.querySelectorAll('.actualizar')
var textbox = document.getElementById('actualizar');

btnsActualizar.forEach(btn=>{
    btn.addEventListener('click', function(e){
      //const valido =verificarContenido(textbox);
      const valido = verificarContenido(textbox);
      if(valido){
        Swal.fire({
          title: 'Desea eliminar este registro?',
          text: "No podra revertir esta accion!",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Si, Eliminar!'
        }).then((result) => {
          if (result.isConfirmed) {
            Swal.fire(
              'Deleted!',
              'Your file has been deleted.',
              'success'
            )
          }
        })
        e.preventDefault();
      }else{
        Swal.fire({
          icon: 'success',
          title: 'Trimestre Actualizado Correctamente',
        })
      }
        
        })
});

function verificarContenido(textbox) {
  var contenido = textbox.value;
  if (contenido.length !== 4) {
    return true;
  } else {
    return false;
  }
}