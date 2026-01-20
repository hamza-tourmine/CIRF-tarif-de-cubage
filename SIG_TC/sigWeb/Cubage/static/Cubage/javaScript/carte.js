
var map = L.map('map').setView([31.791702, -7.09262], 5);
map.zoomControl.setPosition('bottomright');

//GET MAPS CENTER
var center=map.getBounds().getCenter();

// COUCHE DE TUILE
var osm=L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    minZoom: 2,
	maxZoom: 22,
}).addTo(map);

var osmHOT = L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
    maxZoom: 19,
    minZoom: 4,
    attribution: '© OpenStreetMap contributors, Tiles style by Humanitarian OpenStreetMap Team hosted by OpenStreetMap France'});

//couche wms

var wms_url="http://localhost:8080/geoserver/Tarif_de_cubage/wms?service=WMS&version=1.1.0&request=GetMap&layers=Tarif_de_cubage%3Aregions&bbox=-17.104957580566406%2C20.771501541137695%2C-0.99875807762146%2C35.92243194580078&width=768&height=722&srs=EPSG%3A4326&styles=&format=application/openlayers"

var region = L.tileLayer.betterWms("http://localhost:8080/geoserver/Tarif_de_cubage/wms", {
    layers: 'Tarif_de_cubage:regions',
    format: 'image/png',
    transparent: true,
    attribution:'',
    minZoom: 4,
});

var canton = L.tileLayer.betterWms("http://localhost:8080/geoserver/Tarif_de_cubage/wms", {
    layers: '	Tarif_de_cubage:canton',
    format: 'image/png',
    transparent: true,
    attribution:'',
    minZoom: 4,
});

var foretmaamora = L.tileLayer.betterWms("http://localhost:8080/geoserver/Tarif_de_cubage/wms", {
    layers: 'Tarif_de_cubage:foretmaamora',
    format: 'image/png',
    transparent: true,
    attribution:'',
    minZoom: 4,
});

var groupemamora = L.tileLayer.betterWms("http://localhost:8080/geoserver/Tarif_de_cubage/wms", {
    layers: 'Tarif_de_cubage:groupemamora',
    format: 'image/png',
    transparent: true,
    attribution:'',
    minZoom: 4,
});

var parcellaires = L.tileLayer.betterWms("http://localhost:8080/geoserver/Tarif_de_cubage/wms", {
    layers: 'Tarif_de_cubage:parcellaire',
    format: 'image/png',
    transparent: true,
    attribution:'',
    minZoom: 4,
});

// Geojson pour le parcellaire
var parcellaire= new L.featureGroup();

var wfs_url='http://localhost:8080/geoserver/Tarif_de_cubage/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=Tarif_de_cubage%3Aparcellaire&outputFormat=application%2Fjson'


var myStyle = {
    "color": "#ff7800",
    'weight': 2,
    'opacity': 1,
    'dashArray': '3',
    'fillOpacity': 0.7
};

async function getWFSgeojson() {
    try {
        const response = await fetch(wfs_url);
        
        return await response.json();
    } catch (err) {
        console.error(err);
    }
}

getWFSgeojson().then(data => {
    var wfsPolylayer = L.geoJSON(data, {
        style: myStyle,
        onEachFeature: function (f, l) {

            
            var customOptions = {
                maxWidth: "1000px",
                className: "customPOP"
            };
            var groupeId = f.properties.groupe_id;
            var cantonId=f.properties.canton_id;
            var groupeNom = "";
            var foretNom= "";
            var cantonNom='';
            var serieNom='';
            for (var i = 0; i < liste_groupe_json.length; i++) {
                if (liste_groupe_json[i].pk === groupeId) {
                    groupeNom = liste_groupe_json[i].fields.nom_groupe;
                    var serieId=liste_groupe_json[i].fields.serie
                    break;
        
                }
            
            
            }

            

           for (var z = 0; z < liste_serie_json.length; z++) {
                if (liste_serie_json[z].pk === serieId) {
                    serieNom = liste_serie_json[z].fields.nom;
                    var foret_id=liste_serie_json[z].fields.foret;
                    break;
        
                }
            
            
            } 

            for (var h = 0; h < liste_foret_json.length; h++) {
                if (liste_foret_json[h].pk === foret_id) {
                    foretNom = liste_foret_json[h].fields.nom;
                    break;
        
                }
            
            
            } 


            
            for (var j = 0; j < liste_canton_json.length; j++) {
                if (liste_canton_json[j].pk === cantonId) {
                    cantonNom = liste_canton_json[j].fields.nom;
                    break;
                }
            }
            var popupContent = `<div ><b>Parcelle: ${f.properties.parcelle}</b><br/>Groupe: ${groupeNom}
            <br/>Canton: ${cantonNom}<br/>Serie: ${serieNom}<br/>Foret: ${foretNom}</div>`;

            l.bindPopup(popupContent);
            l.bindTooltip(popupContent);
        }
    }).addTo(parcellaire);
});

        
        


/*fetch(wfs_url)
    .then(response => response.json())
    .then(data => {
        const geojsonData = data;
        
        // Créer une couche GeoJSON avec des options de style et l'ajouter à la carte
        const geojsonLayer = L.geoJSON(geojsonData, {
            style: myStyle
        }).addTo(map);

        // Parcourir chaque couche de la couche GeoJSON
        geojsonLayer.eachLayer(function(layer) {
            // Récupérer les propriétés du polygone pour afficher dans l'étiquette
            var properties = layer.feature.properties;
            // Créer une étiquette avec les informations souhaitées
            var label = "Parcelle:" + properties.parcelle; // Remplacez properties.label par le nom de votre propriété contenant l'étiquette

            // Ajouter une étiquette au polygone
            layer.bindTooltip(label);
        });
    }); 


function autreFonction(geojsonData) {
        console.log(geojsonData);
        // Vous pouvez ajouter votre logique supplémentaire ici
    }
*/




//ECHELLE

L.control.scale({position:'bottomleft'}).addTo(map);






//control des couche
var basemaps={
    
    "OSM": osm,
    "OpenStreetMap.HOT": osmHOT,
}

var maps={

    'Parcelles wms':parcellaires,
    'Parcelles wfs':parcellaire,
    'Groupes':groupemamora,
    'canton':canton, 
    'Foret':foretmaamora,
    'Limite des regions du Maroc': region,
    
}

var layersControl = L.control.layers(basemaps, maps);
layersControl.addTo(map);


//____________________________________________________________________________________________________________________________

//fullscreen

var mapid=document.getElementById("map");
function fullscreenView() {
    mapid.requestFullscreen();
}

//map print
//document.querySelector('.print_map').addEventListener('click', function() { window.print();});

var browserControl = L.control.browserPrint({position:'bottomright'}).addTo(map);

//position layer control
layersControl.setPosition('bottomright');

//ZOOM TO LAYER
//document.querySelector('.zoomlayer').addEventListener('click', function() {
 //   map.setView([31.791702, -7.09262], 5);;
 //   });

 //____________________________________________________________________________________________________________________________

//Fonction pour la recherche
function clearResultat(){
    document.getElementById("search-value").value="";
    if (qlayer !=null)
        {map.removeLayer(qlayer)};
    map.setView(center, 5);

}

var qlayer;

 function searchWFS(){
    queryBox=document.getElementById("search-value").value;
    alert(queryBox);
    if(!queryBox){
        alert("Please enter valide input!");
        return false;
    }

    var cqlfilter = "&CQL_FILTER=canton_id='" + queryBox + "'";
    var wfs_urls='http://localhost:8080/geoserver/Tarif_de_cubage/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=Tarif_de_cubage%3Aparcellaire&outputFormat=application%2Fjson' + cqlfilter;

    var myStylecql = {
        "color": "red",
        'weight': 2,
        'opacity': 1,
        'dashArray': '3',
        'fillOpacity': 0.7
    };
    
    async function getgeojson() {
        try {
            const response = await fetch(wfs_urls);
            
            return await response.json();
        } catch (err) {
            console.error(err);
        }
    }

    
    getgeojson().then(data => {
        if(data.totalFeatures > 0){
            qlayer = L.geoJSON(data, {
            style: myStylecql,
            onEachFeature: function (f, l) {
    
                
                var groupeId = f.properties.groupe_id;
                var cantonId=f.properties.canton_id;
                var groupeNom = "";
                var foretNom= "";
                var cantonNom='';
                var serieNom='';
                for (var i = 0; i < liste_groupe_json.length; i++) {
                    if (liste_groupe_json[i].pk === groupeId) {
                        groupeNom = liste_groupe_json[i].fields.nom_groupe;
                        var serieId=liste_groupe_json[i].fields.serie
                        break;
            
                    }
                
                
                }
    
                
    
               for (var z = 0; z < liste_serie_json.length; z++) {
                    if (liste_serie_json[z].pk === serieId) {
                        serieNom = liste_serie_json[z].fields.nom;
                        var foret_id=liste_serie_json[z].fields.foret;
                        break;
            
                    }
                
                
                } 
    
                for (var h = 0; h < liste_foret_json.length; h++) {
                    if (liste_foret_json[h].pk === foret_id) {
                        foretNom = liste_foret_json[h].fields.nom;
                        break;
            
                    }
                
                
                } 
    
    
                
                for (var j = 0; j < liste_canton_json.length; j++) {
                    if (liste_canton_json[j].pk === cantonId) {
                        cantonNom = liste_canton_json[j].fields.nom;
                        break;
                    }
                }
                var popupContent = `<div><b>Parcelle: ${f.properties.parcelle}</b><br/>Groupe: ${groupeNom}
                <br/>Canton: ${cantonNom}<br/>Serie: ${serieNom}<br/>Foret: ${foretNom}</div>`;
    
                l.bindPopup(popupContent);
                l.bindTooltip(popupContent);
                
            }
        }).addTo(map);
        map.fitBounds(qlayer.getBounds()); }
        else{
            alert('Sorry, no resulat found!')
        }
    });
    

 }


 if(!navigator.geolocation) {
        console.log("Your browser doesn't support geolocation feature!")
    } else {
        setInterval(() => {
            navigator.geolocation.getCurrentPosition(getPosition)
        }, 5000);
    }

    var marker, circle;

    function getPosition(position){
        // console.log(position)
        var lat = position.coords.latitude
        var long = position.coords.longitude
        var accuracy = position.coords.accuracy

        if(marker) {
            map.removeLayer(marker)
        }

        if(circle) {
            map.removeLayer(circle)
        }

        marker = L.marker([lat, long])
        circle = L.circle([lat, long], {radius: accuracy})

        var featureGroup = L.featureGroup([marker, circle]).addTo(map)

       

        console.log("Your coordinate is: Lat: "+ lat +" Long: "+ long+ " Accuracy: "+ accuracy)

        
    }

