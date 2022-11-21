$("#id_EstadoSolicitud").change(function(){
    if($(this).val()=="13")
    {    
        $("#dni").show();

    }
     else
     {
         $("#dni").hide();
     }
 });