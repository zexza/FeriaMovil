var url = "https://api.minetools.eu/ping/play.netocraft.xyz";
$.getJSON(url, function(r) {
    //data is the JSON string
 if(r.error){
    $('#rest').html('Server Apagado');
   return false;
 } 
var pl = '';
 if(r.players.sample.length > 0 )
  $('#rest').html(r.description.replace(/§(.+?)/gi, '')+'<br><b><b class="online">●</b>Contectados:</b> '+r.players.online+pl);
 $('#favicon').attr('src', r.favicon);

});