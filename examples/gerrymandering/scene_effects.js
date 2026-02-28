/* Scene effects: grid overlays, dim, court cross, wheel hijack, mobile camera.
 * Reads configuration from window.llmapsData.sceneConfig and
 * window.llmapsData.mobileOverrides. */
(function() {
    var cfg = (window.llmapsData || {}).sceneConfig || {};
    var introIdx = cfg.introIdx || 0;
    var toolsIdx = cfg.toolsIdx || 1;
    var paCtxIdx = cfg.paCtxIdx || 2;
    var courtIdx = cfg.courtIdx || 8;
    var sceneIds = cfg.sceneIds || [];

    /* Mobile camera overrides: default + exceptions */
    var defaultMobile = { center: [-77.62915, 41.07845], zoom: 5.61 };
    var mobileExceptions = (window.llmapsData || {}).mobileOverrides || {
        goofy:   { center: [-75.68084, 40.12504], zoom: 7.87 },
        new_d7:  { center: [-75.68084, 40.12504], zoom: 7.87 },
        packing: { center: [-75.15, 40.0], zoom: 8.5 },
        cracking:{ center: [-75.55869, 40.16528], zoom: 7.87 }
    };

    function isMobile() {
        return window.matchMedia("(max-width: 768px)").matches;
    }

    function forEachStoryMap(callback) {
        var mainMap = window.llmapsStoryMap;
        if (mainMap) callback(mainMap);

        var comparison = window.llmapsStoryComparison;
        if (comparison && comparison.beforeMap) callback(comparison.beforeMap);
        if (comparison && comparison.afterMap) callback(comparison.afterMap);
    }

    function applyMobileCamera(sceneId) {
        if (!isMobile()) return;
        var view = (sceneId && mobileExceptions[sceneId]) || defaultMobile;
        if (!view) return;

        forEachStoryMap(function(map) {
            if (!map || typeof map.flyTo !== "function") return;
            map.flyTo({
                center: view.center,
                zoom: view.zoom,
                duration: 0,
                essential: true,
            });
        });
    }

    var introEl = document.getElementById("grid-overlay-intro");
    var toolsEl = document.getElementById("grid-overlay-tools");
    var courtEl = document.getElementById("court-cross");
    var dimOverlay = document.getElementById("map-dim-overlay");
    var gridBackdrop = document.getElementById("grid-overlay-backdrop");
    var narrative = document.querySelector(".llmaps-story-narrative");
    var steps = narrative ? narrative.querySelectorAll(".story-step") : [];

    function setActiveStep(index) {
        if (!steps || steps.length === 0) return;
        steps.forEach(function(step, i) {
            step.classList.toggle("is-active", i === index);
        });
    }

    function applyScene(index, sceneId) {
        var showGridBackdrop = index === introIdx || index === toolsIdx;

        if (introEl) introEl.classList.toggle("is-visible", index === introIdx);
        if (toolsEl) toolsEl.classList.toggle("is-visible", index === toolsIdx);
        if (gridBackdrop) gridBackdrop.classList.toggle("is-visible", showGridBackdrop);

        if (courtEl) {
            if (index === courtIdx) {
                if (!courtEl.classList.contains("is-visible")) {
                    courtEl.classList.add("is-visible");
                }
            } else {
                courtEl.classList.remove("is-visible");
                void courtEl.offsetWidth;  /* force reflow for animation restart */
            }
        }

        if (dimOverlay) {
            dimOverlay.classList.toggle("is-visible", index === paCtxIdx);
        }

        setActiveStep(index);

        var resolvedSceneId = sceneId || sceneIds[index] || null;
        applyMobileCamera(resolvedSceneId);
    }

    window.addEventListener("llmaps:storySceneChanged", function(evt) {
        var detail = evt.detail || {};
        var idx = Number(detail.index);
        if (Number.isFinite(idx)) applyScene(idx, detail.sceneId || null);
    });

    /* Initial state */
    applyScene(0, sceneIds[0] || null);

    /* ── Wheel hijack: one scroll tick = one scene (desktop only) ── */
    var currentStep = 0;
    var wheelLocked = false;
    var LOCK_MS = 700;

    function scrollToStep(idx) {
        if (idx < 0 || idx >= steps.length) return;
        currentStep = idx;
        applyScene(idx, sceneIds[idx] || null);
        steps[idx].scrollIntoView({ behavior: "smooth", block: "start" });
    }

    if (narrative && steps.length > 0 && !isMobile()) {
        narrative.addEventListener("wheel", function(e) {
            e.preventDefault();
            if (wheelLocked) return;
            var dir = e.deltaY > 0 ? 1 : -1;
            var next = currentStep + dir;
            if (next < 0 || next >= steps.length) return;
            wheelLocked = true;
            scrollToStep(next);
            setTimeout(function() { wheelLocked = false; }, LOCK_MS);
        }, { passive: false });

        window.addEventListener("llmaps:storySceneChanged", function(evt) {
            var idx = Number((evt.detail || {}).index);
            if (Number.isFinite(idx)) currentStep = idx;
        });
    }
})();
