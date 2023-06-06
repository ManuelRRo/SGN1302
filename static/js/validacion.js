const btnsActualizar = document.querySelectorAll('.actualizar')
var textbox = document.getElementById('actualizar');

btnsActualizar.forEach(btn=>{
    btn.addEventListener('click', function(e){
      //const valido =verificarContenido(textbox);
      const valido = true
      if(!valido){
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'Something went wrong!',
          timer: 1500,
        })
        e.preventDefault();
       console.log(valido)
      }else{
        console.log(valido)
      }
        
        })
});

function verificarContenido(textbox) {
  var contenido = textbox.value;
  if (contenido.length === 4) {
    return true;
  } else {
    return false;
  }
}