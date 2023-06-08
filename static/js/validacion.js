const btnsActualizar = document.querySelectorAll('.actualizar')
var textbox = document.getElementById('actualizar');

btnsActualizar.forEach(btn=>{
    btn.addEventListener('click', function(e){
      //const valido =verificarContenido(textbox);
      const valido = verificarContenido(textbox);
      if(valido){
        textbox.setCustomValidity("mensaje de prueba");
        e.preventDefault();
      }else{
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