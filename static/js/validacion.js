const botonUpdateTrim = document.getElementById('trimUpdate');
const botonUpdateEva = document.getElementById('updateEva');
botonUpdateEva.addEventListener('click', validarUpdateEva);
botonUpdateTrim.addEventListener('click', validarCamposUpdateTrim);


function validarCamposUpdateTrim() {
  const anio = document.getElementById('updaterYearTrim');
  const nombre = document.getElementById('updateNombreTrim');
  const aniovalido = validarAnio(anio);
  if(nombre.value.trim().length === 0){
    nombre.setCustomValidity("Ingrese nombre"); 
  }else{
    nombre.setCustomValidity("");
  }
  if (!aniovalido) {
    anio.setCustomValidity("Debe ser un número de 4 dígitos");
  } else {
    anio.setCustomValidity("");
  }
}
function validarAnio(anio) {
  var contenido = anio.value;
  if (contenido.length !== 4) {
    return false; 
  } else {
    return true; 
  }
}

function validarUpdateEva(){
  const nombreEva = document.getElementById('nameUpdateEva');
  const porcentajeEva = document.getElementById('percentageUpdateEva');
  if(nombreEva.value.trim().length ===0){
    nombreEva.setCustomValidity('Ingrese Nombre de Evaluacion');
  }else{
    nombreEva.setCustomValidity('');
  }
  if(porcentajeEva.value.trim().length===0){
    porcentajeEva.setCustomValidity('Ingrese Porcentaje de Evaluacion');
  }else{
    porcentajeEva.setCustomValidity('');
  }
  //if(parseInt(porcentajeEva.value)>25 || parseInt(porcentajeEva.value)<5){
    //porcentajeEva.setCustomValidity('El procentaje no puede ser mayor que 25 y menor que 5');
  //}else{
    //porcentajeEva.setCustomValidity('');
  //}
}