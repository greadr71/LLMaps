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
    var defaultMobile = { center: [-77.58875, 41.15961], zoom: 5.40 };
    var mobileExceptions = (window.llmapsData || {}).mobileOverrides || {
        goofy:   { center: [-75.67962, 40.14411], zoom: 7.60 },
        new_d7:  { center: [-75.67962, 40.14411], zoom: 7.60 },
        packing: { center: [-75.15, 40.0], zoom: 8.5 },
        cracking:{ center: [-75.56075, 40.16843], zoom: 7.12 }
    };
    var hintCfg = (window.llmapsData || {}).scrollHintConfig || {};
    var hintTexts = hintCfg.texts || {};

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
    var hintEl = null;
    var hintTimer = null;
    var hintScrollTarget = null;
    var hintShowDelayMs = Number(hintCfg.showDelayMs);

    if (!Number.isFinite(hintShowDelayMs) || hintShowDelayMs < 0) hintShowDelayMs = 900;

    function canShowHint() {
        return !!narrative && currentStep === 0;
    }

    function getHintText(key) {
        return hintTexts[key] || "";
    }

    function setHintContent(el, msg, mode) {
        if (!el) return;
        if (el.textContent !== msg) el.textContent = msg;
        var nextStyle = mode === "next" && !isMobile();
        el.classList.toggle("is-next", nextStyle);
        el.classList.toggle("is-scroll", !nextStyle);
    }

    function ensureHintEl() {
        if (!canShowHint()) return null;
        if (hintEl) return hintEl;
        hintEl = document.createElement("div");
        hintEl.className = "story-scroll-hint";
        hintEl.setAttribute("role", "note");
        hintEl.setAttribute("aria-live", "polite");
        narrative.appendChild(hintEl);
        return hintEl;
    }

    function hideHint() {
        if (hintTimer) {
            clearTimeout(hintTimer);
            hintTimer = null;
        }
        if (hintEl) hintEl.classList.remove("is-visible");
    }

    function getActiveScrollContainer() {
        var swiper = window.llmapsStorySwiper;
        if (isMobile() && swiper && swiper.slides && swiper.slides.length) {
            var activeSlide = swiper.slides[swiper.activeIndex];
            if (!activeSlide) return narrative;
            return activeSlide.querySelector(".slide-scroll-inner") || narrative;
        }
        return narrative;
    }

    function hasNextScene() {
        return currentStep >= 0 && currentStep < steps.length - 1;
    }

    function isAtBottom(scrollEl) {
        if (!scrollEl) return false;
        var maxScrollTop = scrollEl.scrollHeight - scrollEl.clientHeight;
        if (maxScrollTop <= 2) return true;
        return scrollEl.scrollTop >= maxScrollTop - 5;
    }

    function resolveHintState() {
        if (!hasNextScene()) return { message: "", mode: "none" };
        var scrollEl = getActiveScrollContainer();
        if (!scrollEl) return { message: "", mode: "none" };
        if (isAtBottom(scrollEl)) {
            return {
                message: isMobile() ? getHintText("next_swipe") : getHintText("next_wheel"),
                mode: "next",
            };
        }
        return { message: getHintText("scroll_down"), mode: "scroll" };
    }

    function onHintScroll() {
        var state = resolveHintState();
        if (!state.message) {
            if (hintEl) hintEl.classList.remove("is-visible");
            return;
        }

        if (isMobile() && state.mode === "scroll") {
            if (hintEl) hintEl.classList.remove("is-visible");
            return;
        }

        var el = ensureHintEl();
        if (!el) return;
        setHintContent(el, state.message, state.mode);
        el.classList.add("is-visible");
    }

    function bindHintScrollTarget() {
        if (hintScrollTarget) {
            hintScrollTarget.removeEventListener("scroll", onHintScroll);
        }
        hintScrollTarget = getActiveScrollContainer();
        if (!hintScrollTarget) return;
        hintScrollTarget.addEventListener("scroll", onHintScroll, { passive: true });
    }

    function scheduleHint() {
        hideHint();
        if (!canShowHint()) return;
        bindHintScrollTarget();
        hintTimer = setTimeout(function() {
            if (!canShowHint()) return;
            var state = resolveHintState();
            if (!state.message) return;
            var el = ensureHintEl();
            if (!el) return;
            setHintContent(el, state.message, state.mode);
            el.classList.add("is-visible");
        }, hintShowDelayMs);
    }

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
        hideHint();
        currentStep = idx;
        applyScene(idx, sceneIds[idx] || null);
        if (isMobile() && window.llmapsStorySwiper && typeof window.llmapsStorySwiper.slideTo === "function") {
            window.llmapsStorySwiper.slideTo(idx, 300);
            return;
        }
        steps[idx].scrollIntoView({ behavior: "smooth", block: "start" });
    }

    window.addEventListener("llmaps:storySceneChanged", function(evt) {
        var idx = Number((evt.detail || {}).index);
        if (Number.isFinite(idx)) currentStep = idx;
        var swiper = window.llmapsStorySwiper;
        if (!swiper || !isMobile()) return;
        if (swiper.activeIndex === idx) return;
        swiper.slideTo(idx, 300, false);
    });

    window.addEventListener("llmaps:storySceneChanged", function() {
        scheduleHint();
    });

    if (narrative) {
        narrative.addEventListener("wheel", hideHint, { passive: true });
    }

    if (narrative && steps.length > 0) {
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
    }

    if (narrative && steps.length > 0 && isMobile() && typeof window.Swiper === "function") {
        var MOBILE_SWIPE_EPS = 5;
        var SWIPE_DEAD_ZONE = 10;
        var SWIPE_STEP_THRESHOLD = 50;

        var swiperRoot = document.createElement("div");
        swiperRoot.className = "swiper story-swiper-mobile";

        var swiperWrapper = document.createElement("div");
        swiperWrapper.className = "swiper-wrapper";

        var stepItems = Array.prototype.slice.call(steps);
        stepItems.forEach(function(stepEl) {
            var slide = document.createElement("div");
            slide.className = "swiper-slide";

            var inner = document.createElement("div");
            inner.className = "slide-scroll-inner";

            slide.appendChild(inner);
            inner.appendChild(stepEl);
            swiperWrapper.appendChild(slide);
        });

        swiperRoot.appendChild(swiperWrapper);

        var progressEl = narrative.querySelector(".llmaps-story-progress-mobile");
        if (progressEl && progressEl.nextSibling) {
            narrative.insertBefore(swiperRoot, progressEl.nextSibling);
        } else {
            narrative.appendChild(swiperRoot);
        }

        window.llmapsStorySwiper = new window.Swiper(swiperRoot, {
            direction: "vertical",
            slidesPerView: 1,
            speed: 300,
            allowTouchMove: false,
            effect: "slide",
            resistanceRatio: 0,
            runCallbacksOnInit: false,
        });

        window.llmapsStorySwiper.on("slideChange", function() {
            var idx = window.llmapsStorySwiper.activeIndex;
            currentStep = idx;
            if (typeof window.llmapsApplySceneByIndex === "function") {
                window.llmapsApplySceneByIndex(idx);
            }
        });

        var gesture = {
            startY: 0,
            deltaY: 0,
            modeDecided: false,
            mode: null,
            startedAtTop: false,
            startedAtBottom: false,
        };

        function getActiveInner() {
            var swiper = window.llmapsStorySwiper;
            if (!swiper || !swiper.slides || !swiper.slides.length) return null;
            var activeSlide = swiper.slides[swiper.activeIndex];
            if (!activeSlide) return null;
            return activeSlide.querySelector(".slide-scroll-inner");
        }

        function atTop(inner) {
            return inner.scrollTop <= MOBILE_SWIPE_EPS;
        }

        function atBottom(inner) {
            var maxScrollTop = inner.scrollHeight - inner.clientHeight;
            return inner.scrollTop >= maxScrollTop - MOBILE_SWIPE_EPS;
        }

        narrative.addEventListener("touchstart", function(e) {
            if (e.touches.length !== 1) return;
            var inner = getActiveInner();
            if (!inner) return;

            gesture.startY = e.touches[0].clientY;
            gesture.deltaY = 0;
            gesture.modeDecided = false;
            gesture.mode = null;
            gesture.startedAtTop = atTop(inner);
            gesture.startedAtBottom = atBottom(inner);
        }, { passive: true });

        narrative.addEventListener("touchmove", function(e) {
            if (e.touches.length !== 1) return;
            var inner = getActiveInner();
            if (!inner) return;

            gesture.deltaY = gesture.startY - e.touches[0].clientY;
            if (!gesture.modeDecided && Math.abs(gesture.deltaY) >= SWIPE_DEAD_ZONE) {
                if (gesture.startedAtBottom && gesture.deltaY > 0) {
                    gesture.mode = "next";
                } else if (gesture.startedAtTop && gesture.deltaY < 0) {
                    gesture.mode = "prev";
                } else {
                    gesture.mode = "scroll";
                }
                gesture.modeDecided = true;
            }

            if (gesture.mode === "next" || gesture.mode === "prev") {
                e.preventDefault();
            }
        }, { passive: false });

        narrative.addEventListener("touchend", function() {
            if (!gesture.modeDecided) return;
            var swiper = window.llmapsStorySwiper;
            if (!swiper) return;

            if (gesture.mode === "next" && gesture.deltaY > SWIPE_STEP_THRESHOLD) {
                swiper.slideNext();
            } else if (gesture.mode === "prev" && gesture.deltaY < -SWIPE_STEP_THRESHOLD) {
                swiper.slidePrev();
            }
        });

        bindHintScrollTarget();
    }

    scheduleHint();
})();
