/* arena-layer.js — the fourth mode: ARENA. The bridge between the globe and the arena.
 *
 * WHY A BRIDGE IS NEEDED AT ALL. Right now they are two estates that do not know about
 * each other. The globe (sovspace) shows six measured axes and a regulatory clock. The
 * arena (os.meok.ai/arena) is a launch-gate list — GovComp, SOVBENCH, the framework gap
 * matrix — and it names exactly ONE of the twelve greenfields. The twelve live on
 * Hugging Face with twelve Spaces and, until today, zero runnable tools.
 *
 * This mode puts all three on one surface: each greenfield is a node, its size is how
 * complete its chain is, its colour is its measured score, and clicking it opens the
 * tool that runs it. The arena's launch gate is respected — a greenfield that is SPEC or
 * DRAFT says so and cannot be read as a result.
 *
 * POSITIONING IS NOT DECORATIVE. Each greenfield sits at the seat of the instrument that
 * creates its obligation, the same rule the axes layer already uses. A benchmark with no
 * statutory anchor sits in the Atlantic, which is the honest place for it.
 *
 * Requires: map, cullMarkers(), stopSpin() from sovspace.html; window.__ARENA__.
 */
(function () {
  "use strict";

  var A = window.__ARENA__;
  if (!A) { console.error("[arena] no data"); return; }

  var MK = [], MODE = false;
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };

  // Chain completeness drives SIZE. Score drives COLOUR. A greenfield that is published
  // everywhere but measured nowhere is big and grey — which is the truth about it.
  function chain(g) {
    var k = ["dataset", "card", "space", "spaceTool", "kaggle", "page", "pageTool",
             "lmeval", "inspect", "measured"];
    return k.filter(function (x) { return g.marks[x]; }).length / k.length;
  }
  /* INSTRUMENT_FAILED is not a low score, it is the absence of one, and it must not
   * render anywhere on the score ramp. A run where the pod dropped 96.7% of connections
   * would otherwise paint red and be read as "the model is bad at governance". It gets
   * its own colour, off the ramp entirely. */
  function colour(g) {
    if (g.status === "INSTRUMENT_FAILED") return "#C9A84C";          // instrument, not model
    if (g.status && g.status !== "MEASURED") return "#8FB3A5";       // SPEC or DRAFT — no score
    if (g.macro_f1 != null) {
      return g.macro_f1 >= 0.6 ? "#34d399" : g.macro_f1 >= 0.4 ? "#fbbf24" : "#f87171";
    }
    // generic score fallback: acc-scored axes carry a numeric score in score_value (metric labelled).
    // Ramp on it WITHOUT coercing acc into macro_f1 (different metric, kept distinct).
    // score_value may be "0.515 acc" — parseFloat reads the leading number, ignores the metric suffix.
    var sv = (g.score_value != null) ? parseFloat(String(g.score_value)) : (g.acc != null ? g.acc : NaN);
    if (!isNaN(sv)) {
      return sv >= 0.6 ? "#34d399" : sv >= 0.4 ? "#fbbf24" : "#f87171";
    }
    return "#60a5fa";                                                // published, no numeric score
  }

  function fc() {
    return { type: "FeatureCollection", features: A.greenfields.map(function (g, i) {
      var c = chain(g);
      return { type: "Feature",
        properties: { i: i, col: colour(g), r: 7 + 26 * c,
                      op: 0.10 + 0.26 * c, chain: Math.round(c * 100) },
        geometry: { type: "Point", coordinates: [g.lng, g.lat] } };
    })};
  }

  function build() {
    if (map.getSource("arena")) return;
    map.addSource("arena", { type: "geojson", data: fc() });
    map.addLayer({ id: "arena-halo", type: "circle", source: "arena",
      layout: { visibility: "none" },
      paint: { "circle-radius": ["interpolate", ["linear"], ["zoom"], 1, ["get", "r"], 5, ["*", 2.2, ["get", "r"]]],
               "circle-color": ["get", "col"], "circle-opacity": ["get", "op"],
               "circle-stroke-color": ["get", "col"], "circle-stroke-width": 1.2,
               "circle-stroke-opacity": 0.62 }});
    map.addLayer({ id: "arena-core", type: "circle", source: "arena",
      layout: { visibility: "none" },
      paint: { "circle-radius": 4.5, "circle-color": ["get", "col"], "circle-opacity": 0.96 }});
    A.greenfields.forEach(function (g, i) {
      var el = document.createElement("div");
      el.className = "mlabel ev"; el.style.display = "none"; el.dataset.vis = "off";
      el.innerHTML = '<b style="color:' + colour(g) + '">' + esc(g.bench) + "</b> " +
                     Math.round(chain(g) * 100) + "%";
      el.onclick = function () { open(i); };
      MK.push(new maplibregl.Marker({ element: el, anchor: "left", offset: [10, 0] })
        .setLngLat([g.lng, g.lat]).addTo(map));
    });
    window.__arenaMarkers = MK;
    ["arena-halo", "arena-core"].forEach(function (l) {
      map.on("click", l, function (e) { open(e.features[0].properties.i); });
      map.on("zoom", declutter);
      map.on("mouseenter", l, function () { map.getCanvas().style.cursor = "pointer"; });
      map.on("mouseleave", l, function () { map.getCanvas().style.cursor = ""; });
    });
  }

  var LINKS = [
    ["dataset",  "items load",      function (g) { return "https://huggingface.co/datasets/csoai/" + g.id; }],
    ["space",    "HF Space",        function (g) { return "https://huggingface.co/spaces/csoai/" + g.id; }],
    ["spaceTool","Space is a tool", null],
    ["kaggle",   "Kaggle",          function (g) { return g.kaggle ? "https://www.kaggle.com/datasets/nicktempleman/" + g.kaggle : null; }],
    ["page",     "site page",       function (g) { return g.page ? "https://csoai.org/" + g.page + ".html" : null; }],
    ["pageTool", "page is a tool",  null],
    ["lmeval",   "lm-eval task",    null],
    ["inspect",  "Inspect task",    null],
    ["measured", "measured",        null],
  ];

  /* THE BOARD. Until now this panel said "sov34 macro-F1 0.386" with no run behind it —
   * a number with no instrument attached, which is the exact claim shape this estate
   * refuses to accept from anyone else. Every row now names its model AND its harness,
   * and a run the instrument could not certify appears as a dropped run with its failure
   * reasons rather than as a low score. */
  function board(g) {
    var rs = g.runs || [], dr = g.dropped_runs || [], h = "";
    if (!rs.length && !dr.length) {
      return g.macro_f1 != null
        ? '<div class="kv"><span>macro-F1</span><span>' + g.macro_f1.toFixed(3) + "</span></div>"
        : "";
    }
    if (rs.length) {
      h += '<div style="margin:10px 0 4px;font-size:10.5px;letter-spacing:.09em;' +
           'text-transform:uppercase;color:#8FB3A5">measured</div>' +
           '<table style="width:100%;border-collapse:collapse;font-size:12px">' +
           '<tr style="color:#8FB3A5;font-size:10px;text-transform:uppercase;letter-spacing:.06em">' +
           "<th style='text-align:left;padding:2px 0'>model</th><th style='text-align:right'>macro-F1</th>" +
           "<th style='text-align:right'>acc 95% CI</th>" +
           "<th style='text-align:right'>unreadable</th><th style='text-align:right'>n</th></tr>";
      rs.forEach(function (r, k) {
        var f = r.macro_f1;
        h += '<tr style="border-top:1px solid #164034' + (k === 0 ? ";font-weight:600" : "") + '">' +
             '<td style="padding:4px 0;color:#ecfdf5">' + esc(r.model) + "</td>" +
             '<td style="text-align:right;color:' +
               (f >= 0.6 ? "#34d399" : f >= 0.4 ? "#fbbf24" : "#f87171") + '">' +
               (f == null ? "—" : f.toFixed(3)) + "</td>" +
             /* The interval prints only where n cleared 30. Everywhere else the cell says
              * n<30 rather than showing a wide interval, because a wide interval on screen
              * still gets quoted — the threshold is on n, not on the width. */
             '<td style="text-align:right;color:' + (r.quotable ? "#ecfdf5" : "#8FB3A5") + '">' +
               (r.quotable && r.accuracy_ci95 && r.accuracy != null
                 ? r.accuracy.toFixed(3) + " [" + r.accuracy_ci95[0].toFixed(3) + ", " +
                   r.accuracy_ci95[1].toFixed(3) + "]"
                 : "n&lt;30") + "</td>" +
             '<td style="text-align:right;color:#8FB3A5">' +
               Math.round((r.unparsed_rate || 0) * 100) + "%</td>" +
             '<td style="text-align:right;color:#8FB3A5">' + (r.n_scored || "—") + "</td></tr>";
      });
      h += "</table>";
      var harnesses = rs.map(function (r) { return r.harness; })
                        .filter(function (v, k, a2) { return a2.indexOf(v) === k; });
      h += '<div style="font-size:10.5px;color:#8FB3A5;margin-top:5px;line-height:1.5">' +
           "via " + esc(harnesses.join(" · ")) +
           (rs.some(function (r) { return r.quotable; })
             ? " · intervals shown only where n reached usable_n = 30"
             : " · below usable_n = 30, so no interval is quoted") + "</div>";
    }
    if (dr.length) {
      h += '<div class="warnbox" style="border-left-color:#C9A84C"><b>' + dr.length +
           " run" + (dr.length > 1 ? "s" : "") + " dropped.</b> " +
           dr.map(function (r) {
             var reasons = Object.keys(r.error_reasons || {}).map(function (k) {
               return k + "×" + r.error_reasons[k]; }).join(", ");
             return esc(r.model) + " at " +
                    Math.round((r.instrument_error_rate || 0) * 100) + "% instrument error" +
                    (reasons ? " (" + esc(reasons) + ")" : "");
           }).join("; ") +
           ". A dropped connection is not a wrong answer, so these contribute no score.</div>";
    }
    return h;
  }

  function open(i) {
    var g = A.greenfields[i];
    map.flyTo({ center: [g.lng, g.lat], zoom: 3.0, duration: 1300, essential: true });
    var done = LINKS.filter(function (l) { return g.marks[l[0]]; }).length;
    var badge =
      g.status === "MEASURED" ? "" :
      g.status === "INSTRUMENT_FAILED"
        ? '<div class="warnbox" style="border-left-color:#C9A84C"><b>Instrument failed.</b> ' +
          'A harness ran against this greenfield and the connection, not the model, is what ' +
          'broke. No score exists. The failure is reported here rather than published as a ' +
          'low result, because those are different claims.</div>'
        : '<div class="warnbox" style="border-left-color:#C9A84C"><b>' + esc(g.status) + '.</b> ' +
          'No score exists on this greenfield yet. The protocol is published so a harness can ' +
          'consume it, and that is all it claims.</div>';
    document.getElementById("detailBody").innerHTML =
      "<h3>" + esc(g.bench) + "</h3>" +
      '<div class="prov">' + esc(g.axis) + " · " + esc(g.seat) + " · " + esc(g.instrument) + "</div>" +
      "<p>" + esc(g.task) + "</p>" +
      '<div class="kv"><span>chain complete</span><span>' + done + "/" + LINKS.length + "</span></div>" +
      (g.n != null ? '<div class="kv"><span>items (n)</span><span>' + g.n + "</span></div>" : "") +
      board(g) +
      badge +
      '<div style="margin-top:12px">' + LINKS.map(function (l) {
        var on = g.marks[l[0]], href = l[2] && l[2](g);
        var label = on && href
          ? '<a href="' + href + '" style="color:#34d399;text-decoration:none">' + l[1] + " ↗</a>"
          : esc(l[1]);
        return '<div style="font-size:12px;padding:5px 0;border-bottom:1px solid #164034;' +
               'opacity:' + (on ? 1 : 0.45) + '">' + (on ? "● " : "○ ") + label + "</div>";
      }).join("") + "</div>" +
      (g.tool
        ? '<div class="acts"><a href="' + esc(g.tool) + '">Run it →</a>' +
          '<a class="ghost" href="https://huggingface.co/datasets/csoai/' + esc(g.id) + '">Dataset</a></div>'
        : '<div class="warnbox">No runnable tool yet on this greenfield.</div>') +
      '<div class="warnbox">Disc size is how much of the chain is complete, not how good the ' +
      'result is. A greenfield published everywhere and measured nowhere renders large and ' +
      'grey, because that is what it is.</div>';
    document.getElementById("detail").classList.add("open");
    document.getElementById("a11y").textContent =
      g.bench + ", " + g.axis + ", chain " + done + " of " + LINKS.length + " complete.";
  }

  function rail() {
    var host = document.getElementById("axes");
    if (!host) return;
    host.innerHTML = "";
    var done = A.greenfields.reduce(function (s, g) { return s + chain(g); }, 0);
    var head = document.createElement("div");
    head.style.cssText = "font-size:11px;color:#8FB3A5;margin:0 0 10px;line-height:1.5";
    var ms = A.models_seen || [];
    head.innerHTML = '<b style="color:#ecfdf5">' + A.greenfields.length + " greenfields · chain " +
      Math.round(done / A.greenfields.length * 100) + "% complete</b><br>" +
      "Size is chain completeness. Colour is the best score any measured model reached, " +
      "grey where nothing is " +
      "measured yet, or gold where the instrument failed and there is no score to show." +
      (ms.length ? "<br>Scored against " + ms.length + " model" + (ms.length > 1 ? "s" : "") +
                   ": " + esc(ms.join(", ")) + "." : "");
    host.appendChild(head);
    A.greenfields.slice().sort(function (a, b) { return chain(b) - chain(a); }).forEach(function (g) {
      var i = A.greenfields.indexOf(g), c = chain(g);
      var b = document.createElement("button");
      b.className = "axis"; b.type = "button";
      b.innerHTML =
        '<span class="top"><span class="dot" style="background:' + colour(g) + '"></span>' +
        '<span class="nm" style="text-transform:none;font-size:13px">' + esc(g.bench) + "</span>" +
        '<span class="f1">' + Math.round(c * 100) + "%</span></span>" +
        /* The headline is the BEST score any measured model reached, which is what tells
         * you how hard the greenfield is. It is not "our model's score", and naming the
         * model inline is what stops it being read that way. */
        '<span class="sub"><span>' + esc(g.measured_model || g.axis) + "</span>" +
        "<span>" + (g.n != null ? "n=" + g.n : "—") + "</span>" +
        '<span' + (g.status !== "MEASURED" ? ' style="color:#C9A84C"' : "") + ">" +
        (g.macro_f1 != null ? g.macro_f1.toFixed(3) : g.status) + "</span></span>" +
        '<span class="bar"><i style="width:' + (c * 100).toFixed(0) + '%;background:' + colour(g) + '"></i></span>';
      b.onclick = function () { open(i); };
      host.appendChild(b);
    });
  }

  /* Four instruments share Brussels and two share London. At world zoom their labels
   * overlap into an unreadable knot — the same failure the clock layer had. Below zoom
   * 2.4 only the greenfields with a measured score are labelled; zoom in and the rest
   * appear. The discs stay visible either way, so nothing is hidden, only unlabelled. */
  function declutter() {
    if (!MODE) return;
    var z = map.getZoom();
    MK.forEach(function (mk, i) {
      var g = A.greenfields[i];
      mk.getElement().style.display = (z >= 2.4 || g.macro_f1 != null) ? "" : "none";
    });
    if (typeof cullMarkers === "function") cullMarkers();
  }

  function setVis(on) {
    MODE = on;
    ["arena-halo", "arena-core"].forEach(function (l) {
      if (map.getLayer(l)) map.setLayoutProperty(l, "visibility", on ? "visible" : "none"); });
    MK.forEach(function (m) {
      var el = m.getElement(); el.dataset.vis = on ? "on" : "off"; el.style.display = on ? "" : "none"; });
    if (on) declutter(); else if (typeof cullMarkers === "function") cullMarkers();
  }

  window.__arena = {
    enter: function () {
      if (typeof stopSpin === "function") stopSpin();
      setVis(true); rail();
      var h2 = document.querySelector("#rail h2");
      if (h2) h2.textContent = "ARENA · 12 GREENFIELDS";
      map.flyTo({ center: [-26, 42], zoom: 1.8, duration: 1200 });
    },
    exit: function () { setVis(false); },
  };

  function start() { build(); window.__arenaReady = true;
    console.log("[arena] " + A.greenfields.length + " greenfields bridged"); }
  if (map.isStyleLoaded()) start(); else map.on("load", start);
})();
