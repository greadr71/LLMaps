/**
 * Browser-side DataDrivenSize math (aligned with llmaps/components/data_driven_size.py).
 * Injected when any layer has metadata.llmaps_data_driven_size_spec.
 *
 * API:
 *   llmapsDataDrivenSizeResolveFromValues(values, spec, options?)
 *   llmapsDataDrivenSizeBuildInterpolate(field, stops, options?)
 *   llmapsApplyDataDrivenSizeFromValues(map, layerId, layerType, values, spec, options?)
 *   llmapsApplyRuntimeStyle(map, layerId, style)
 *   llmapsApplyRuntimeStyles(map, styles)
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

  function pick(obj, snakeName, camelName, defaultValue) {
    if (!obj) return defaultValue;
    if (Object.prototype.hasOwnProperty.call(obj, snakeName)) return obj[snakeName];
    if (Object.prototype.hasOwnProperty.call(obj, camelName)) return obj[camelName];
    return defaultValue;
  }

  function normalizeSpec(spec, extra) {
    var input = spec || {};
    var opts = extra || {};
    return {
      field: pick(input, 'field', 'field', pick(opts, 'field', 'field', null)),
      sizeRange: pick(input, 'size_range', 'sizeRange', pick(opts, 'size_range', 'sizeRange', [4, 22])),
      autoPercentiles: pick(
        input,
        'auto_percentiles',
        'autoPercentiles',
        pick(opts, 'auto_percentiles', 'autoPercentiles', [0.1, 0.5, 0.9])
      ),
      minValue: pick(input, 'min_value', 'minValue', pick(opts, 'min_value', 'minValue', null)),
      maxValue: pick(input, 'max_value', 'maxValue', pick(opts, 'max_value', 'maxValue', null)),
      filterPositive: !!pick(input, 'filter_positive', 'filterPositive', pick(opts, 'filter_positive', 'filterPositive', false))
    };
  }

  function collectFiniteValues(values, filterPositive) {
    var arr = [];
    if (!values) return arr;

    if (typeof Symbol !== 'undefined' && values && typeof values[Symbol.iterator] === 'function') {
      var it = values[Symbol.iterator]();
      var step;
      while (!(step = it.next()).done) {
        var v = Number(step.value);
        if (!isFinite(v)) continue;
        if (filterPositive && v <= 0) continue;
        arr.push(v);
      }
      return arr;
    }

    if (Array.isArray(values) || typeof values.length === 'number') {
      for (var i = 0; i < values.length; i++) {
        var x = Number(values[i]);
        if (!isFinite(x)) continue;
        if (filterPositive && x <= 0) continue;
        arr.push(x);
      }
    }
    return arr;
  }

  function resolveFromValues(values, spec, extra) {
    var normalized = normalizeSpec(spec, extra);
    var arr = collectFiniteValues(values, normalized.filterPositive);
    if (!arr.length) return null;
    arr.sort(function (a, b) { return a - b; });

    var pStops = normalized.autoPercentiles || [0.1, 0.5, 0.9];
    var pv0 = percentileSorted(arr, pStops[0]);
    var pv1 = percentileSorted(arr, pStops[1]);
    var pv2 = percentileSorted(arr, pStops[2]);
    if (pv0 == null || pv1 == null || pv2 == null) return null;

    var minV = normalized.minValue;
    var maxV = normalized.maxValue;
    var v0 = minV != null && isFinite(Number(minV)) ? Number(minV) : pv0;
    var v2 = maxV != null && isFinite(Number(maxV)) ? Number(maxV) : pv2;
    var v1 = pv1;
    var tri = [v0, v1, v2].sort(function (a, b) { return a - b; });
    v0 = tri[0];
    v1 = tri[1];
    v2 = tri[2];
    if (!(v2 > v0)) return null;

    var lo = Number((normalized.sizeRange || [4, 22])[0]);
    var hi = Number((normalized.sizeRange || [4, 22])[1]);
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
    var normalized = normalizeSpec(spec, options || {});
    var field = normalized.field;
    if (!field) return null;
    var expr = buildInterpolate(field, stops, { coalesceDefault: !!(options && options.coalesceDefault) });
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

  function applyRuntimeStyle(map, layerId, style) {
    var cfg = style || {};
    if (!map || !layerId || !map.getLayer(layerId)) return false;
    try {
      var paint = cfg.paint || {};
      Object.keys(paint).forEach(function (name) {
        map.setPaintProperty(layerId, name, paint[name]);
      });

      var layout = cfg.layout || {};
      Object.keys(layout).forEach(function (name) {
        map.setLayoutProperty(layerId, name, layout[name]);
      });

      var filter = cfg.filter;
      if (filter != null && typeof map.setFilter === 'function') {
        map.setFilter(layerId, filter);
      }
    } catch (e) {
      if (typeof console !== 'undefined' && console.warn) {
        console.warn('[llmapsRuntimeStyle]', layerId, e);
      }
      return false;
    }
    return true;
  }

  function applyRuntimeStyles(map, styles) {
    var applied = {};
    if (!styles) return applied;
    Object.keys(styles).forEach(function (layerId) {
      applied[layerId] = applyRuntimeStyle(map, layerId, styles[layerId]);
    });
    return applied;
  }

  global.llmapsDataDrivenSizeResolveFromValues = resolveFromValues;
  global.llmapsDataDrivenSizeBuildInterpolate = buildInterpolate;
  global.llmapsApplyDataDrivenSizeFromValues = applyFromValues;
  global.llmapsDataDrivenSizePercentileSorted = percentileSorted;
  global.llmapsApplyRuntimeStyle = applyRuntimeStyle;
  global.llmapsApplyRuntimeStyles = applyRuntimeStyles;
})(typeof window !== 'undefined' ? window : typeof global !== 'undefined' ? global : this);
