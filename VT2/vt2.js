window.onload = function() {

  luoSisalto();
  ruudukonLuonti(8, 8);
  window.addEventListener("resize", resize, false);
  // Estetään submit-nappulan oletustoiminta
  document.getElementsByTagName("input")[1].addEventListener('click', stopDefAction, false);
  // Lisätään submit-nappulalle uusi eventkuuntelija
  document.getElementsByTagName("input")[1].addEventListener('click', luoRuudukko, false);  
}

// Globaalit muuttujat
var alkukoko = 8;
var klikattuSpannitesti;
var pelikaynnissa = true;
var handled = false;
var vuoro = 1;              // Annetaan vuoro pelaajalle 1 aina alussa
var syonti = false;
var syotavaNappula;


// Muutetaan Breakthrough-laudan kokoa selaimen ikkunan koon mukaan
function resize() {
    var body = document.body,
    html = document.documentElement;

    var height = Math.max( body.scrollHeight, body.offsetHeight, 
                       html.clientHeight, html.scrollHeight, html.offsetHeight );

   var h1 = document.getElementsByTagName('h1');
   var form = document.getElementsByTagName('form');
   
   // Huomioidaan myös muut elementit
   var height1 = h1[0].offsetTop + h1[0].scrollHeight + form[0].offsetTop + form[0].scrollHeight;
   var heightLopullinen = height1 + alkukoko;   
   var cellHeight = (height - heightLopullinen) / alkukoko;
   
   var cells = document.getElementsByTagName("td");
   for (i = 0; i < cells.length; i++) {
      cells[i].setAttribute("width", cellHeight);
      cells[i].setAttribute("height", cellHeight);
  }
   
}

// Luodaan formi jossa kysytään laudan koko
function luoSisalto() {
   
   var body = document.getElementsByTagName("body");
   
   var pteksti = document.createElement("p");
   var teksti = document.createTextNode("Kerro luotavan ruudukon koko. Ruudukko on yhtä monta ruutua leveä kuin korkea.");
   pteksti.appendChild(teksti);
   body[0].appendChild(pteksti);
   
   var form = document.createElement("form");
   form.setAttribute("action", " ");
   form.setAttribute("id", "ruudukko");
   body[0].appendChild(form);
   
   var fieldset = document.createElement("fieldset");
   form.appendChild(fieldset);
   
   var p1 = document.createElement("p");
   fieldset.appendChild(p1);
   
   var label = document.createElement("label");
   var textnode = document.createTextNode("Leveys ");
   p1.appendChild(label);
   var input1 = document.createElement("input");
   input1.setAttribute("type", "text");
   input1.setAttribute("name", "x");
   label.appendChild(textnode);
   label.appendChild(input1);
   
   var p2 = document.createElement("p");
   form.appendChild(p2);
   var input2 = document.createElement("input");
   input2.setAttribute("type", "submit")
   input2.setAttribute("value", "Luo");
   p2.appendChild(input2);
}


// Estetään submit-nappulan normaali toiminta
function stopDefAction(e) {
   e.preventDefault();
}


// Käsitellään käyttäjän syöty ja tarkistetaan ikkunan koko
function luoRuudukko() {
   
   var x = document.getElementsByName("x");
   var leveys = x[0].value;
   var leveys2 = parseInt(leveys);
   
   var body = document.body,
    html = document.documentElement;

   var height = Math.max( body.scrollHeight, body.offsetHeight, 
                       html.clientHeight, html.scrollHeight, html.offsetHeight );
					   
   // Tarkistetaan onko annettu ruudukon koko väliltä 8 ja 32
   // jos on kutsutaan ruudukonluonti funktiota
   if (leveys2 >= 8 && leveys2 <= 32) {
   
      ruudukonLuonti(leveys2, alkukoko);
	  
      alkukoko = leveys2;
   }
   
}


// Funktio ruudukon luontiin
function ruudukonLuonti(x, alku) {
   pelikaynnissa = true;
   vuoro = 1;
   
   var tables = document.getElementsByTagName("table");
   if (tables.length !== 0) {
   // Poistetaan vanha taulukko kun luodaan uusi pelikenttä uuteen peliin
   var body = document.getElementsByTagName("body");
     body[0].removeChild(tables[0]);  
   }
   
   var body = document.getElementsByTagName("body");
   var table = document.createElement("table");
   body[0].appendChild(table);
   table.style.borderSpacing = "0";
   
   var body = document.body,
    html = document.documentElement;

   var height = Math.max( body.scrollHeight, body.offsetHeight, 
                       html.clientHeight, html.scrollHeight, html.offsetHeight );

   var h1 = document.getElementsByTagName('h1');
   var form = document.getElementsByTagName('form');
   var height1 = h1[0].offsetTop + h1[0].scrollHeight + form[0].offsetTop + form[0].scrollHeight;
   var heightLopullinen = height1 + x;   
   var cellHeight = (height - heightLopullinen) / x;
   for (i = 0; i < x; i++){
      var row = table.insertRow(i);
      for (a = 0; a < x; a++){
	     // Annetaan jokaiselle solulle attribuutit ja tyyli
	     var cell = row.insertCell(a);
		 cell.style.border = "1px solid black";
		 cell.setAttribute("width", cellHeight);
	     cell.setAttribute("height", cellHeight);
		 cell.style.padding = "0";
		 cell.style.margin = "0";
		 // Lisätään myös tapahtumankäsittelijä
		 cell.addEventListener("click", nappulanSiirto, false);
		 if ( i % 2 == 0 && a % 2 !== 0) {
			
			cell.style.backgroundColor = "black";
         }
         else if (i % 2 !== 0 && a % 2 == 0) {
			cell.style.backgroundColor = "black";
         }
        
		// Pelaajan 1 nappulat (Ylemmät)
		if (i == 0 || i == 1) {
		  var span = document.createElement("span");
		  span.setAttribute("class", "pelaaja1");
		  cell.appendChild(span);
		  span.addEventListener("click", nappulanValinta, true)
		  span.style.background = "radial-gradient(ellipse at center, #f0f9ff 0%, #cbebff 47%, #a1dbff 100%)"
		 }
		 // Pelaajan 2 nappulat (Alemmat)
		 else if (i > x-3) {		 
		   var span = document.createElement("span");
		   span.setAttribute("class", "pelaaja2");
		   cell.appendChild(span);
		   span.addEventListener("click", nappulanValinta, true)
		   span.style.background = "radial-gradient(ellipse at center, #fff9f0 0%, #ffebcb 47%, #ffdba1 100%)"
		 }
	  }
   }
   
   // Asetetaan kaikilla nappuloille tyylit
   var spans = document.getElementsByTagName("span");
   for (i = 0; i < spans.length; i++) {
	  spans[i].style.padding = "0";
	  spans[i].style.height = "80%";
	  spans[i].style.width = "80%";
	  spans[i].style.display = "block";
	  spans[i].style.borderRadius = "50%";
	  spans[i].style.marginLeft = "auto";
	  spans[i].style.marginRight = "auto";
	  
   }
}


// Funktio jossa käsitellään nappulan valinta
function nappulanValinta(eventObj) {
   if (pelikaynnissa) {
      handled = true;
      var klikattuSolu = eventObj.target.parentNode.cellIndex;
      var klikattuRivi = eventObj.target.parentNode.parentNode.rowIndex;
      if (vuoro == 1 && eventObj.target.className == "pelaaja2" && klikattuSpannitesti !== undefined && klikattuSpannitesti !== null){
         var nappulaSolu = klikattuSpannitesti.parentNode.cellIndex;
	     var nappulaRivi = klikattuSpannitesti.parentNode.parentNode.rowIndex;
	     if (klikattuRivi - nappulaRivi == 1 && (nappulaSolu - klikattuSolu == 1 || nappulaSolu - klikattuSolu == -1)) {
	        syotavaNappula = eventObj.target;	 
	     }
	     handled = false;
         return;
      }
      if (vuoro == 2 && eventObj.target.className == "pelaaja1" && klikattuSpannitesti !== undefined && klikattuSpannitesti !== null) {
	     var nappulaSolu = klikattuSpannitesti.parentNode.cellIndex;
	     var nappulaRivi = klikattuSpannitesti.parentNode.parentNode.rowIndex;
         if (klikattuRivi - nappulaRivi == -1 && (nappulaSolu - klikattuSolu == 1 || nappulaSolu - klikattuSolu == -1)) {
	        syotavaNappula = eventObj.target;
	     }
	     handled = false;
         return;
      }   
     // klikattuSpannitesti = eventObj.target;
      if (vuoro == 1 && eventObj.target.className == "pelaaja1") {
	     klikattuSpannitesti = eventObj.target;
         var spans = document.getElementsByClassName("valittu");
	        if (spans.length !== 0) {
	           spanni = spans[0];
	           spanni.setAttribute("class", "pelaaja1");
		       spanni.style.border = "0px"; 
	        }
      klikattuSpannitesti.setAttribute("class", "valittu");
	  klikattuSpannitesti.style.border = "2px solid red";
      return;	  
      }
      else if (vuoro == 2 && eventObj.target.className == "pelaaja2") {
	     klikattuSpannitesti = eventObj.target;
         var spans = document.getElementsByClassName("valittu");
	     if (spans.length !== 0) {
	        spanni = spans[0];
	        spanni.setAttribute("class", "pelaaja2");
		    spanni.style.border = "0px";
         }
	     klikattuSpannitesti.setAttribute("class", "valittu"); 
	     klikattuSpannitesti.style.border = "2px solid red";
	     return;
      }  
   }
}


// Funktio käsittelee nappulan siirtämisen
function nappulanSiirto(eventObj) {
   if (pelikaynnissa) {
      var siirretty = false;
      if (handled !== true) {
         // Tarkistetaan onko nappula aiheuttanut tapahtuman ja jos on niin otetaan muuttujaan sen vanhempi
         if (eventObj.target.tagName == "SPAN"){
	        var cell = eventObj.target.parentNode;
	     }
	     else var cell = eventObj.target;
	     
		 // Nappula syönti
	     if (klikattuSpannitesti !== undefined && klikattuSpannitesti !== null && eventObj.target.tagName == "SPAN" && syotavaNappula !== undefined && syotavaNappula !== null) {	     
	        syotavaNappula.parentNode.removeChild(syotavaNappula);	
            syotavaNappula = null;		 
	     }
      	 
		 // Liikutukseen liittyvä algoritmi
	     if (cell.children.length == 0 && klikattuSpannitesti !== undefined && klikattuSpannitesti !== null){
	        var siirryttavaCell = cell.cellIndex;
		    var siirryttavaRow = cell.parentNode.rowIndex;
		    var alkuCell = klikattuSpannitesti.parentNode.cellIndex;
		    var alkuRivi = klikattuSpannitesti.parentNode.parentNode.rowIndex;
			// Pelaajan 1 liiktussäännöt
            if (vuoro == 1 && siirryttavaRow - alkuRivi == 1 && (siirryttavaCell - alkuCell == 1 || siirryttavaCell - alkuCell == -1 || siirryttavaCell - alkuCell == 0 )) {	  
	           cell.appendChild(klikattuSpannitesti);
			   siirretty = true;
			
			   if (klikattuSpannitesti.parentNode.parentNode.rowIndex == alkukoko - 1) {
			      pelikaynnissa = false;
			      klikattuSpannitesti.style.background = "radial-gradient(ellipse at center, black 0%, red 47%, blue 100%)"
			   }
		    }
		    
			// Pelaajan 2 liiktussäännöt
		    if (vuoro == 2 && siirryttavaRow - alkuRivi == -1 && (siirryttavaCell - alkuCell == 1 || siirryttavaCell - alkuCell == -1 || siirryttavaCell - alkuCell == 0 )) {
		       cell.appendChild(klikattuSpannitesti);
			   siirretty = true;
			
			   if (klikattuSpannitesti.parentNode.parentNode.rowIndex == 0) {
			      pelikaynnissa = false;
			      klikattuSpannitesti.style.background = "radial-gradient(ellipse at center, black 0%, red 47%, blue 100%)"
			   }
		    }
		 	
         // Poistetaan valinta ja vaihdetaan vuoro siirron jälkeen			
	     if (vuoro == 1 && siirretty == true) {	     
	        klikattuSpannitesti.setAttribute("class", "pelaaja1");
	        klikattuSpannitesti.style.border = "0px";
	      	vuoro = 2;
	   	    klikattuSpannitesti = null;
		    siirretty = false;
   	     }
	     if (vuoro == 2 && siirretty == true) {	    
	        klikattuSpannitesti.setAttribute("class", "pelaaja2");
	        klikattuSpannitesti.style.border = "0px";
	        vuoro = 1;
	        klikattuSpannitesti = null;
	        }
         }
      }
      else handled = false;
    }  
}