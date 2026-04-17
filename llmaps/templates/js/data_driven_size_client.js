/**
 * Browser-side DataDrivenSize math (aligned with llmaps/components/data_driven_size.py).
 * Injected when any layer has metadata.llmaps_data_driven_size_spec.
 *
 * API:
 *   llmapsDataDrivenSizeResolveFromValues(values, spec, options?)
 *   llmapsDataDrivenSizeBuildInterpolate(field, stops, options?)
 *   llmapsApplyDataDrivenSizeFromValues(map, layerId, layerType, values, spec, options?)
 */
(function (global) {
  'use strict';

  function percentileSorted(sortedArr, p) {
    if (!sortedArr || sortedArr.length === 0) return null;
    var pp = Number(p);
    if (!isFinite(pp)) return null;
    pp = Math.max(0, Math.min(1, pp));
    var n = sortedArr.length;
    if (n === 1) return sortedArr[0];
    var idx = (n - 1) * pp;
    var lo = Math.floor(idx);
    var hi = Math.ceil(idx);
    if (lo === hi) return sortedArr[lo];
    var t = idx - lo;
    return sortedArr[lo] * (1 - t) + sortedArr[hi] * t;
  }

  function resolveFromValues(values, spec, extra) {
    extra = extra || {};
    var filterPositive = !!extra.filterPositive;
    var arr = [];
    if (Array.isArray(values)) {
      for (var i = 0; i < values.length; i++) {
        var x = Number(values[i]);
        if (!isFinite(x)) continue;
        if (filterPositive && x <= 0) continue;
        arr.push(x);
      }
    }
    if (!arr.length) return null;
    arr.sort(function (a, b) { return a - b; });

    var pStops = spec.auto_percentiles || [0.1, 0.5, 0.9];
    var pv0 = percentileSorted(arr, pStops[0]);
    var pv1 = percentileSorted(arr, pStops[1]);
    var pv2 = percentileSorted(arr, pStops[2]);
    if (pv0 == null || pv1 == null || pv2 == null) return null;

    var minV = spec.min_value;
    var maxV = spec.max_value;
    var v0 = minV != null && isFinite(Number(minV)) ? Number(minV) : pv0;
    var v2 = maxV != null && isFinite(Number(maxV)) ? Number(maxV) : pv2;
    var v1 = pv1;
    var tri = [v0, v1, v2].sort(function (a, b) { return a - b; });
    v0 = tri[0];
    v1 = tri[1];
    v2 = tri[2];
    if (!(v2 > v0)) return null;

    var lo = Number((spec.size_range || [4, 22])[0]);
    var hi = Number((spec.size_range || [4, 22])[1]);
    var t1 = (v2 - v0) === 0 ? 0 : (v1 - v0) / (v2 - v0);
    var s0 = lo;
    var s2 = hi;
    var s1 = s0 + t1 * (s2 - s0);
    return { v0: v0, v1: v1, v2: v2, s0: s0, s1: s1, s2: s2 };
  }

  function buildInterpolate(field, stops, opts) {
    opts = opts || {};
    var inner = ['to-number', ['get', field], 0];
    if (opts.coalesceDefault) {
      inner = ['coalesce', inner, 0];
    }
    return [
      'interpolate',
      ['linear'],
      inner,
      stops.v0, stops.s0,
      stops.v1, stops.s1,
      stops.v2, stops.s2
    ];
  }

  function applyFromValues(map, layerId, layerType, values, spec, options) {
    var stops = resolveFromValues(values, spec, options || {});
    if (!stops || !map || !map.getLayer(layerId)) return null;
    var expr = buildInterpolate(spec.field, stops, { coalesceDefault: !!(options && options.coalesceDefault) });
    try {
      if (layerType === 'circle') {
        map.setPaintProperty(layerId, 'circle-radius', expr);
      } else if (layerType === 'symbol') {
        map.setLayoutProperty(layerId, 'icon-size', expr);
      } else {
        return null;
      }
    } catch (e) {
      if (typeof console !== 'undefined' && console.warn) {
        console.warn('[llmapsDataDrivenSize]', layerId, e);
      }
      return null;
    }
    return stops;
  }

  global.llmapsDataDrivenSizeResolveFromValues = resolveFromValues;
  global.llmapsDataDrivenSizeBuildInterpolate = buildInterpolate;
  global.llmapsApplyDataDrivenSizeFromValues = applyFromValues;
})(typeof window !== 'undefined' ? window : typeof global !== 'undefined' ? global : this);
