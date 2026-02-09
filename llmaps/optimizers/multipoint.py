"""
MULTIPOINT explosion for LLMaps.

Expands MULTIPOINT geometries into separate Point features in chunks
to avoid blocking the UI when loading large GeoJSON.
"""


def generate_multipoint_explosion_js() -> str:
    """
    Generate JavaScript for expanding MULTIPOINT into separate Point features.

    Processes features in chunks (setTimeout) so the main thread stays responsive.

    Returns
    -------
    str
        JS code defining explodeMultiPoint(geojson, callback).
    """
    return r"""      function explodeMultiPoint(geojson, callback) {
        if (!geojson || !geojson.features || !geojson.features.length) {
          callback(geojson || { type: "FeatureCollection", features: [] });
          return;
        }
        const features = [];
        let processed = 0;
        const total = geojson.features.length;
        const chunkSize = 100;
        function processChunk() {
          const end = Math.min(processed + chunkSize, total);
          for (let i = processed; i < end; i++) {
            const feature = geojson.features[i];
            if (feature.geometry && feature.geometry.type === "MultiPoint") {
              feature.geometry.coordinates.forEach(coord => {
                features.push({
                  type: "Feature",
                  geometry: { type: "Point", coordinates: coord },
                  properties: feature.properties || {}
                });
              });
            } else {
              features.push(feature);
            }
          }
          processed = end;
          if (processed < total) setTimeout(processChunk, 0);
          else callback({ type: "FeatureCollection", features });
        }
        processChunk();
      }"""
