(function($){
	$(document).ready(function() 
	{
	valor = $('.field-legalizada select').val();
    if (valor == 'Si') {
      $('#documentopropiedad_set-group').show();
    } else if (valor == 'No') {
      $('#documentopropiedad_set-group').hide();
    } else {
      $('#documentopropiedad_set-group').hide();
    }

    $('.field-legalizada select').change(function(){

      valor = $('.field-legalizada select').val();
      if (valor == 'Si') {
	      $('#documentopropiedad_set-group').show();
	    } else {
	      $('#documentopropiedad_set-group').hide();
	    }
      });

    valor1 = $('.field-mano_obra select').val();
    if (valor1 == 'Si') {
      $('#tablaempleo_set-group').show();
    } else if (valor1 == 'No') {
      $('#tablaempleo_set-group').hide();
    } else {
      $('#tablaempleo_set-group').hide();
    }

    $('.field-mano_obra select').change(function(){

      valorq = $('.field-mano_obra select').val();
      if (valorq == 'Si') {
	      $('#tablaempleo_set-group').show();
	    } else {
	      $('#tablaempleo_set-group').hide();
	    }
      });

    valor2 = $('.field-respuesta select').val();
    if (valor2 == 'Si') {
      $('#respuestasicotiza_set-group').show();
    } else if (valor2 == 'No') {
      $('#respuestasicotiza_set-group').hide();
    } else {
      $('#respuestasicotiza_set-group').hide();
    }

    $('.field-respuesta select').change(function(){

      valor2 = $('.field-respuesta select').val();
      if (valor2 == 'Si') {
	      $('#respuestasicotiza_set-group').show();
	    } else {
	      $('#respuestasicotiza_set-group').hide();
	    }
      });

    valor3 = $('#id_beneficiadoproyecto_set-0-respuesta').val();
    if (valor3 == 'Si') {
      $('#beneficiadoproyecto_set-0 .field-proyectos').show();
     } else {
      $('#beneficiadoproyecto_set-0 .field-proyectos').hide();
    }

     $('.field-respuesta #id_beneficiadoproyecto_set-0-respuesta').change(function(){

      valor3 = $('.field-respuesta #id_beneficiadoproyecto_set-0-respuesta').val();
      if (valor3 == 'Si') {
	      $('#beneficiadoproyecto_set-0.field-proyectos').show();
	     } else {
	      $('#beneficiadoproyecto_set-0.field-proyectos').hide();
	    }
      });

     valor4 = $('#id_miembrocooperativa_set-0-respuesta').val();
    if (valor4 == 'Si') {
      $('.field-cooperativa').show();
     } else {
      $('.field-cooperativa').hide();
    }

     $('.field-respuesta #id_miembrocooperativa_set-0-respuesta').change(function(){

      valor4 = $('.field-respuesta #id_miembrocooperativa_set-0-respuesta').val();
      if (valor4 == 'Si') {
	      $('.field-cooperativa').show();
	     } else {
	      $('.field-cooperativa').hide();
	    }
      });

     valor5 = $('#id_credito_set-0-respuesta').val();
    if (valor5 == 'Si') {
      $('#credito_set-group .field-proyectos').show();
      $('#credito_set-group .field-formas_recibe_credito').show();
     } else {
      $('#credito_set-group .field-proyectos').hide();
      $('#credito_set-group .field-formas_recibe_credito').hide();
    }

     $('.field-respuesta #id_credito_set-0-respuesta').change(function(){

      valor5 = $('.field-respuesta #id_credito_set-0-respuesta').val();
      if (valor5 == 'Si') {
	      $('#credito_set-group .field-proyectos').show();
	      $('#credito_set-group .field-formas_recibe_credito').show();
	     } else {
	      $('#credito_set-group .field-proyectos').hide();
	      $('#credito_set-group .field-formas_recibe_credito').hide();
	    }
      });

	});
})(jQuery || django.jQuery);