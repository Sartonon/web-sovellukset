// Globaalit muuttujat
var alustus = 0;
var idtaulukko = [];
var tietotaulukko = [];
var tyyppitaulukko = [];
var lajitaulukko = [];
var muokattavaID;
var kirjaudu;
var kirjautunutEmail;
var kirjautunutNimi;

window.onload = function() {
   autentikoi();
   $("#kirjaudunappula").on("click", autentikoi)
   $("#kirjaudunappula").on("click", stopDefAction, false)
   $("#rekisteroi").on("click", rekisteroituminen)
   $("#takaisin").on("click", stopDefAction, false)
   $("#tallennarek").on("click", stopDefAction, false)
   $("#takaisin").on("click", takaisin)
   $("#tallennarek").on("click", rekisteroi)
   $("#uloskirjaus").on("click", kirjaaUlos)
   $("#lisaa").on("click", tarkistasyotteet);
   $("#lisaa").on("click", stopDefAction, false);
   
}

function kirjauduUlos() {
}

// Funktio takaisin-nappulalle rekisteröitymisessä
function takaisin() {
    var h2 = document.getElementById("rek");
    h2.setAttribute("class", "hidden");
    var reki = document.getElementById("rekisterointi")
    reki.setAttribute("class", "hidden");
    var div = document.getElementById("kirjaudu");
    div.setAttribute("class", "");
    var div2 = document.getElementById("paasivu");
    div2.setAttribute("class", "hidden");
}


function rekisteroituminen() {
    var reki = document.getElementById("rekisterointi")
    reki.setAttribute("class", "");
    var div = document.getElementById("kirjaudu");
    div.setAttribute("class", "hidden");
}

// Rekisteröinti, tarkistetaan kentät ja jos ok niin rekisteröidään
function rekisteroi() {
    var onkoOk = false;
    if (  $('#nimi').val() != "" &&  $('#sukunimi').val() != "" 
         &&  $('#uusitunnus').val() != "" &&  $('#uusisalasana1').val() != "" 
         &&  $('#uusisalasana2').val() != "") {
        if ($('#uusisalasana1').val() == $('#uusisalasana2').val()) {
            onkoOk = true;
        }
    }
    else {
        var vaarin = document.getElementById("vaarinr");
        vaarin.setAttribute("class", "");
    }
    
    if (onkoOk) {
       $.ajax({ 
      	async: true,
      	url: "rekisterointi.py", 
      	data: {"etunimi": $('#nimi').val(), "sukunimi": $("#sukunimi").val(), "uusitunnus": $("#uusitunnus").val(),
       "uusisalasana": $("#uusisalasana1").val() },    
      	processData: true,
      	dataType: "text",
      	type: "GET",
      	success: rekisteroitu,
      	error: ajax_virhe
      });
    }
    
}


function autentikoi() {
   kirjaudu = this.value;
   $.ajax({ 
   	async: true,
   	url: "autentikointi.py", 
   	data: {"tunnus": $('#tunnus').val(), "salasana": $("#salasana").val()},    
   	processData: true,
   	dataType: "text",
   	type: "GET",
   	success: kirjautuminen,
   	error: ajax_virhe
   });
    
}


function rekisteroitu(data) {
    document.getElementById("form3").reset();
    var vaarin = document.getElementById("vaarinr");
    vaarin.setAttribute("class", "hidden");
    var h2 = document.getElementById("rek");
    h2.setAttribute("class", "");
}


function kirjaaUlos() {
    $.ajax({ 
   	async: true,
   	url: "invalidoi.py",    
   	processData: true,
   	dataType: "text",
   	type: "GET",
   	success: kirjauduttuUlos,
   	error: ajax_virhe
   });
   
}


function kirjauduttuUlos(data) {
       var h2 = document.createElement("h2");
       h2.setAttribute("id", "ilmoitus");
       h2.setAttribute("class", "hidden")
       $( "#ilmoitus" ).replaceWith( h2 );
       var div = document.getElementById("kirjaudu");
       div.setAttribute("class", "");
       var div2 = document.getElementById("paasivu");
       div2.setAttribute("class", "hidden");
}

// Tarkistetaan tiedot kirjautuessa ja päästetään sisään jos ok
function kirjautuminen(data) {
   document.getElementById("form2").reset();
   var reki = document.getElementById("rekisterointi")
   reki.setAttribute("class", "hidden");
   //console.log(data);
   var lol = document.getElementById("vaarin");
   var data2 = data;
   // Paloitellaan tullut data
   if (data.indexOf("|") > -1){
      var datasplit = data.split("|");
      kirjautunutEmail = datasplit[0];
      kirjautunutNimi = datasplit[1];
      data2 = datasplit[2];
      //console.log(kirjautunutEmail);
   }
   
   if (data == -2) {
       var div = document.getElementById("kirjaudu");
       div.setAttribute("class", "");
       var div2 = document.getElementById("paasivu");
      div2.setAttribute("class", "hidden");
       
   }
   
   if (data2 == -2 && kirjaudu != "Kirjaudu!") {
       var div = document.getElementById("kirjaudu");
       div.setAttribute("class", "");
   }
   
   if (data2 == -2 && kirjaudu == "Kirjaudu!") {
      
      lol.setAttribute("class", "");
   }
   
   if (data2 == 0) {
      lol.setAttribute("class", "hidden");
      var div = document.getElementById("kirjaudu");
      div.setAttribute("class", "hidden");
      var div2 = document.getElementById("paasivu");
      div2.setAttribute("class", "");
      
      listaa_treenit();
      listaa_lajit();
      listaa_treenityypit();
      //listaa_henkilot();
     
      //document.getElementById("lisaa").addEventListener('click', stopDefAction, false)
      $("#poista").on("click", tyhjennaTreenit);
      $('#defaultSlider').on("input", muutaArvoa);
      $('#defaultSlider').on("change", muutaArvoa);
      $('#defaultSlider').change();
      $("#kesto").on("input", laske);
      $("#km").on("input", laske);
   }
}

// Funktio joka laskee kahdesta inputista nopeuden ja laittaa sen ruutuun
function laske() {
    if ( $("#kesto").val() != 0 && $("#km").val() != 0) {
       var a = $("#kesto").val();
       var b = $("#km").val();
       var c = Math.round(a/b * 100) / 100;
       $("#output").val(c + " min/km");
    }
    else {
        $("#output").val(0);
    }
    
}


// Estetään submit-nappulan normaali-toiminta
function stopDefAction(evt) {
  evt.preventDefault();
}


// Muutetaan sliderin arvoa
function muutaArvoa(event, ui) {
   var currentValue = $('#currentValue');
   currentValue.html(this.value);
}


function tyhjennaTreenit() {
   $.ajax({ 
	async: true,
	url: "tyhjenna_treenit.py",
	dataType: "text",
	type: "GET",
	success: treenittyhjennetty,
	error: ajax_virhe
});
}

function treenittyhjennetty(data, textStatus, request) {
    
}



function poistaLataus() {
   $("#kuvake").empty();
}


function lisaaLataus() {
   var image = document.createElement("img");
   image.setAttribute("src", "ajax-loader.gif");
   var span = document.getElementById("kuvake");
   span.appendChild(image); 
}


function lisaa_treenit() {
lisaaLataus();
$.ajax({ 
	async: true,
	url: "lisaa_treeni.py", 
 	data: {"treenityyppi": $('#treenit').val(), "laji": $("#lajit").val(), "alkuluku": $('#alkuluku').val(), "email": kirjautunutEmail,
    "kesto": $('#kesto').val(),
    "km": $('#km').val(),
    "keskisyke": $('#defaultSlider').val(),
    "sykemax": $('#sykemax').val(),
    "kalorit": $('#kalorit').val(),
    "kommentti": $('#kommentti').val() },    
	processData: true,
	dataType: "text",
	type: "GET",
	success: lisatty,
	error: ajax_virhe
});
}


function listaa_treenit() {
$.ajax({ 
	async: true,
	url: "listaa_treenit.py",
	dataType: "json",
	type: "GET",
	success: listaatreenit,
	error: ajax_virhe
});
}


function listaa_treenityypit() {
$.ajax({ 
	async: true,
	url: "listaa_treenityypit.py",
	dataType: "json",
	type: "GET",
	success: listaatreenityypit,
	error: ajax_virhe
});
}

/*function listaa_henkilot() {
$.ajax({ 
	async: true,
	url: "listaa_henkilot.py",
	dataType: "json",
	type: "GET",
	success: listaahenkilot,
	error: ajax_virhe
});
} */


function listaa_lajit() {
$.ajax({ 
	async: true,
	url: "listaa_lajit.py",
	dataType: "json",
	type: "GET",
	success: listaalajit,
	error: ajax_virhe
});
}


function ajax_virhe(event, jqxhr, settings, exception) {
 console.log( exception );
}


// Laitetaan ilmoitus onnistuneesta treenin lisäyksestä
function lisatty(data, textStatus, request) {
        poistaLataus();
        var h2 = document.createElement("h2");
        h2.setAttribute("id", "ilmoitus");
        text = document.createTextNode("Lisätty kantaan onnistuneesti");
        h2.appendChild(text);
        $( "#ilmoitus" ).replaceWith( h2 );
        listaa_treenit();
        document.getElementById("form").reset();
        $('#defaultSlider').change();
}


function listaahenkilot(data) {
  /* var select = document.getElementById("henkilot");
   var i = 0
   $.each( data, function( key, val ) {
     var option = document.createElement("option");
     if (i == 0) {
        option.setAttribute("selected", "selected")
        i++;
     }
     var splitattu = val.split("|");
     option.setAttribute("value", key);
     textnode1 = document.createTextNode(splitattu[0] + " " + splitattu[1]);
     option.appendChild(textnode1);
     select.appendChild(option);
   }); */
}

// Listaa lajit select-valikkoon
function listaalajit(data) {
   var select = document.getElementById("lajit");
   lajitaulukko = [];
   $.each( data, function( key, val ) {
     var tietue = [];
     tietue.push(key);
     tietue.push(val);
     lajitaulukko.push(tietue);
     var option = document.createElement("option");
     option.setAttribute("value", key);
     textnode = document.createTextNode(val);
     option.appendChild(textnode);
     select.appendChild(option);
   });
}

// Listaa treenityypit select-valikkoon
function listaatreenityypit(data) {
   var select = document.getElementById("treenit");
   tyyppitaulukko = [];
   $.each( data, function( key, val ) {
     var tietue = [];
     tietue.push(key);
     tietue.push(val);
     tyyppitaulukko.push(tietue);
     var option = document.createElement("option");
     option.setAttribute("value", key);
     textnode = document.createTextNode(val);
     option.appendChild(textnode);
     select.appendChild(option);
   });
}



function listaatreenit(data) {
    var table = document.getElementById("taulukkorunko");
    idtaulukko = [];
    tietotaulukko = [];
    $('#taulukkorunko').empty();
     
    $.each( data, function( key, val ) {
    
    var tr = document.createElement("tr");
    table.appendChild(tr);
    var splitattu = val.split("|")
    idtaulukko.push(splitattu[0]);
    //console.log(splitattu);
    var tiedot = "";
    for (i = 1; i < splitattu.length; i++) {
        tiedot += splitattu[i];
        if ( i != splitattu.length - 1) {
           tiedot += "|";
        }
        var td = document.createElement("td");
        text = document.createTextNode(splitattu[i]);
        td.appendChild(text);
        tr.appendChild(td);
    }
    tietotaulukko.push(tiedot);
    id = splitattu[0];
    //console.log(id);
    if (splitattu[1] == kirjautunutNimi) {
       var muokkaa = document.createElement("button");
       muokkaa.setAttribute("value", id);
       text = document.createTextNode("Muokkaa");
       muokkaa.appendChild(text);
       muokkaa.addEventListener("click", muokkaaTreenia);
       var td = document.createElement("td");
       td.appendChild(muokkaa);
       tr.appendChild(td);
       
       var poista = document.createElement("button");
       poista.setAttribute("value", id);
       text = document.createTextNode("Poista");
       poista.appendChild(text);
       poista.addEventListener("click", poistaTreeni);
       var td = document.createElement("td");
       td.appendChild(poista);
       tr.appendChild(td);
    }
    
       // var option = document.createElement("option");
       // option.setAttribute("value", key );
       // option.appendChild( document.createTextNode( val ));
       // select.append(option); // select on jquery-olio joten on käytettävä jqueryn tarjoamaa metodia

});
     //console.log(idtaulukko);
     //console.log(tietotaulukko);
     var resort = true;
     $("#treenilistaus").trigger("update", [resort]);
     
     if (alustus == 0 && tietotaulukko.length != 0) {
         $("#treenilistaus").tablesorter({sortList: [[0,0], [3,1]]});
         alustus++;
     }
     //$("#treenilistaus").trigger("sorton", [[3,1]]);
     
}


function muokkaaTreenia() {
   muokattavaID = this.value;
   //console.log("Muokataan treeniä: " + this.value);
   var indeksi;
   for (i = 0; i < idtaulukko.length; i++) {
      if (idtaulukko[i] == this.value) {
         indeksi = i;
         //console.log("onnistui: " + "indeksi on: " + indeksi)
         break;
      }
   }
   
   var split = tietotaulukko[indeksi].split("|");
   
   /*for (i = 0; i < split.length; i++) {
       
   } */
   //console.log(lajitaulukko);
   for (i = 0; i < tyyppitaulukko.length; i++) {
       if (split[1] == tyyppitaulukko[i][1]) {
           $("#treenit").val(tyyppitaulukko[i][0])
           break;
       }
   }
   
   for (i = 0; i < lajitaulukko.length; i++) {
       if (split[2] == lajitaulukko[i][1]) {
           $("#lajit").val(lajitaulukko[i][0])
           break;
       }
   }
   
   
   $("#alkuluku").val(split[3]);
   $("#kesto").val(split[4]);
   $("#km").val(split[5]);
   $("#defaultSlider").val(split[7]);
   $('#defaultSlider').change();
   $("#sykemax").val(split[8]);
   $("#kalorit").val(split[9]);
   $("#kommentti").val(split[10]);
   
   var lisaa = $("#lisaa");
   //console.log(tyyppitaulukko);
   
   
   var muokkaa = document.createElement("input");
   muokkaa.setAttribute("type", "submit");
   muokkaa.setAttribute("value", "Tallenna");
   muokkaa.setAttribute("id", "tallenna");
   //$("#tallenna").on("click", stopDefAction, false)
   muokkaa.addEventListener('click', stopDefAction, false)
   muokkaa.addEventListener("click", muokkaa_treenia)
   
   lisaa.replaceWith(muokkaa);
   
}

// Tarkistetaan onko kentät ok ja tehdään ajax-kutsu jo on
function muokkaa_treenia() {
    if ( $('#alkuluku').val() != "" && $('#kesto').val() != "" && $('#km').val() != "" 
     && $('#keskisyke').val() != "" && $('#sykemax').val() != "" && $('#kalorit').val() != ""
     && $('#kommentti').val() != "") {
         lisaaLataus();
        $.ajax({ 
    	async: true,
    	url: "muokkaa_treeni.py", 
     	data: {"id": muokattavaID, "treenityyppi": $('#treenit').val(), "laji": $("#lajit").val(), "alkuluku": $('#alkuluku').val(), "email": kirjautunutEmail,
        "kesto": $('#kesto').val(),
        "km": $('#km').val(),
        "keskisyke": $('#defaultSlider').val(),
        "sykemax": $('#sykemax').val(),
        "kalorit": $('#kalorit').val(),
        "kommentti": $('#kommentti').val() },    
    	processData: true,
    	dataType: "text",
    	type: "GET",
    	success: tallennettu,
    	error: ajax_virhe
    });
     }
     else {
        var h2 = document.createElement("h2");
        h2.setAttribute("id", "ilmoitus");
        h2.setAttribute("class", "red");
        text = document.createTextNode("Ei tallennettu tietokantaan, syötä kaikki tiedot!");
        h2.appendChild(text);
        $( "#ilmoitus" ).replaceWith( h2 );
        //$("#ilmoitus").replaceWith(newElem);
        
     }
    
}

// Tallennuksen onnistuminen
function tallennettu() {
   var muokkaa = $("#tallenna");
   var lisaa = document.createElement("input");
   lisaa.setAttribute("type", "submit");
   lisaa.setAttribute("value", "Lisää Treeni");
   lisaa.setAttribute("id", "lisaa");
   //$("#tallenna").on("click", stopDefAction, false)
   lisaa.addEventListener('click', stopDefAction, false)
   lisaa.addEventListener("click", tarkistasyotteet)
   muokkaa.replaceWith(lisaa);
   listaa_treenit();
   poistaLataus();
   document.getElementById("form").reset();
   $('#defaultSlider').change();
   var h2 = document.createElement("h2");
   h2.setAttribute("id", "ilmoitus");
   text = document.createTextNode("Tiedot muutettu tietokantaan onnistuneesti!");
   h2.appendChild(text);
   $( "#ilmoitus" ).replaceWith( h2 ); 
}



function poistaTreeni() {
   lisaaLataus();
   $.ajax({ 
	async: true,
	url: "poista_treeni.py", 
 	data: {"treeniid": this.value},    
	processData: true,
	dataType: "text",
	type: "GET",
	success: poistettu,
	error: ajax_virhe
});
}


function poistettu() {
   var h2 = document.createElement("h2");
   h2.setAttribute("id", "ilmoitus");
   text = document.createTextNode("Treeni poistettu kannasta onnistuneesti!");
   h2.appendChild(text);
   $( "#ilmoitus" ).replaceWith( h2 );
   listaa_treenit();
   poistaLataus();
}


// Tarkistaa onko kaikkiin kenttiin syötetty jotain
function tarkistasyotteet() {
    if ( $('#alkuluku').val() != "" && $('#kesto').val() != "" && $('#km').val() != "" 
     && $('#keskisyke').val() != "" && $('#sykemax').val() != "" && $('#kalorit').val() != ""
     && $('#kommentti').val() != "") {
         lisaa_treenit();
         //var h2 = document.createElement("h2");
         //h2.setAttribute("id", "ilmoitus2");
         //text = document.createTextNode("Lisätty kantaan onnistuneesti");
         //h2.appendChild(text);
         //$( "#ilmoitus2" ).replaceWith( h2 );
     }
     else {
        var h2 = document.createElement("h2");
        h2.setAttribute("id", "ilmoitus");
        h2.setAttribute("class", "red");
        text = document.createTextNode("Ei lisätty tietokantaan, syötä kaikki tiedot!");
        h2.appendChild(text);
        $( "#ilmoitus" ).replaceWith( h2 );
        //$("#ilmoitus").replaceWith(newElem);
        
     }
}