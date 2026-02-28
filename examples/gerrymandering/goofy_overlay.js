/* Goofy image overlay on the comparison "after" map.
 * Reads configuration from window.llmapsData.goofyConfig:
 *   { imageDataUrl, bounds, sceneIndex } */
(function() {
    var cfg = (window.llmapsData || {}).goofyConfig || {};
    var overlaySourceId = "goofy-overlay-source";
    var overlayLayerId = "goofy-overlay-layer";
    var imageDataUrl = cfg.imageDataUrl;
    var imageBounds = cfg.bounds;
    var goofySceneIndex = cfg.sceneIndex;
    var afterMapRef = null;

    if (!imageDataUrl || !imageBounds) return;

    function getActiveSceneIndexFromDom() {
        var active = document.querySelector(".story-step.is-active");
        if (!active) return -1;
        var idx = Number(active.dataset.index);
        return Number.isFinite(idx) ? idx : -1;
    }

    function setOverlayVisible(map, visible) {
        if (!map || !map.getLayer(overlayLayerId)) return;
        map.setLayoutProperty(overlayLayerId, "visibility", visible ? "visible" : "none");
    }

    function syncOverlayVisibility(sceneIndex) {
        if (!afterMapRef) return;
        var idx = Number.isFinite(sceneIndex) ? sceneIndex : getActiveSceneIndexFromDom();
        setOverlayVisible(afterMapRef, idx === goofySceneIndex);
    }

    function ensureOverlay(map) {
        if (!map.getSource(overlaySourceId)) {
            map.addSource(overlaySourceId, {
                type: "image",
                url: imageDataUrl,
                coordinates: imageBounds,
            });
        }

        if (!map.getLayer(overlayLayerId)) {
            map.addLayer({
                id: overlayLayerId,
                type: "raster",
                source: overlaySourceId,
                paint: {
                    "raster-opacity": 0.88,
                    "raster-fade-duration": 0,
                },
                layout: {
                    visibility: "none",
                },
            });
        }
    }

    function attachToMap(map) {
        if (!map || map === afterMapRef) return;
        afterMapRef = map;

        function init() {
            ensureOverlay(afterMapRef);
            syncOverlayVisibility();
        }

        if (typeof map.loaded === "function" && map.loaded()) {
            init();
        } else {
            map.on("load", init);
        }
        map.on("styledata", init);
    }

    function tryAttachFromGlobal() {
        var g = window.llmapsStoryComparison;
        if (g && g.afterMap) attachToMap(g.afterMap);
    }

    window.addEventListener("llmaps:storyComparisonReady", function(evt) {
        var detail = evt.detail || {};
        if (detail.afterMap) attachToMap(detail.afterMap);
    });

    window.addEventListener("llmaps:storySceneChanged", function(evt) {
        var detail = evt.detail || {};
        var idx = Number(detail.index);
        syncOverlayVisibility(Number.isFinite(idx) ? idx : undefined);
    });

    tryAttachFromGlobal();
    setTimeout(tryAttachFromGlobal, 300);
    setTimeout(tryAttachFromGlobal, 1000);
})();
