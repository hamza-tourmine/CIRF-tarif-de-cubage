L.TileLayer.BetterWMS = L.TileLayer.WMS.extend({
  
    onAdd: function (map) {
      // Triggered when the layer is added to a map.
      //   Register a click listener, then do all the upstream WMS things
      L.TileLayer.WMS.prototype.onAdd.call(this, map);
      map.on('click', this.getFeatureInfo, this);
    },
    
    onRemove: function (map) {
      // Triggered when the layer is removed from a map.
      //   Unregister a click listener, then do all the upstream WMS things
      L.TileLayer.WMS.prototype.onRemove.call(this, map);
      map.off('click', this.getFeatureInfo, this);
    },
    
    getFeatureInfo: function (evt) {
    // Make an AJAX request to the server and hope for the best
    var url = this.getFeatureInfoUrl(evt.latlng),
      showResults = L.Util.bind(this.showGetFeatureInfo, this);
    $.ajax({
      url: url,
      success: function (data, status, xhr) {
        var err = typeof data === 'string' ? null : data;
        //Fix for blank popup window
        var doc = (new DOMParser()).parseFromString(data, "text/html"); 
        if (doc.body.innerHTML.trim().length > 0)
          showResults(err, evt.latlng, data);
      },
      error: function (xhr, status, error) {
        showResults(error);
      }
    });
  },
    
    getFeatureInfoUrl: function (latlng) {
      // Construct a GetFeatureInfo request URL given a point
      var point = this._map.latLngToContainerPoint(latlng, this._map.getZoom()),
          size = this._map.getSize(),
          
          params = {
            request: 'GetFeatureInfo',
            service: 'WMS',
            srs: 'EPSG:4326',
            styles: this.wmsParams.styles,
            transparent: this.wmsParams.transparent,
            version: this.wmsParams.version,      
            format: this.wmsParams.format,
            bbox: this._map.getBounds().toBBoxString(),
            height: size.y,
            width: size.x,
            layers: this.wmsParams.layers,
            query_layers: this.wmsParams.layers,
            info_format: 'text/html'
          };
      
      params[params.version === '1.3.0' ? 'i' : 'x'] = point.x;
      params[params.version === '1.3.0' ? 'j' : 'y'] = point.y;
      
      return this._url + L.Util.getParamString(params, this._url, true);
    },
    
    showGetFeatureInfo: function (err, latlng, content) {
      if (err) { 
        console.error(err); 
        return; // Ne rien faire en cas d'erreur
      }
    
      // Parse la réponse du serveur
      var parser = new DOMParser();
      var xmlDoc = parser.parseFromString(content, "text/html");
    
      // Récupère la valeur de la propriété "nom"
      var nom = xmlDoc.querySelector("table.featureInfo tr:nth-child(2) td:nth-child(5)").textContent.trim();
    
      // Crée le contenu à afficher dans la fenêtre contextuelle
      var popupContent = "<b>Région:</b> " + nom;
    
      // Affiche la fenêtre contextuelle sur la carte
      L.popup({ maxWidth: 800})
        .setLatLng(latlng)
        .setContent(popupContent)
        .openOn(this._map);
    }
    
    
  });
  
  L.tileLayer.betterWms = function (url, options) {
    return new L.TileLayer.BetterWMS(url, options);  
  };