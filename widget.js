/* Council OS embeddable widget — add ONE script tag to any website.
 * Simpler: (function(){...}) auto-injects a measured-governance panel.
 * Drop: <script src="https://csoai-gspc.pages.dev/widget.js" data-axis="care" async></script>
 */
(function(){
  var ax = (document.currentScript && document.currentScript.getAttribute('data-axis')) || 'care';
  var host = 'https://csoai-gspc.pages.dev';
  var b = document.createElement('button');
  b.textContent = '🛡 Council OS';
  b.style.cssText = 'position:fixed;bottom:16px;right:16px;z-index:999999;background:#10161d;color:#7cc7a1;border:1px solid #2e3e4f;border-radius:999px;padding:.55rem 1rem;font:600 .8rem system-ui;cursor:pointer;box-shadow:0 6px 22px rgba(0,0,0,.35)';
  b.onclick = function(){
    var w = window.open(host + '/?axis=' + ax, 'csoai-widget', 'width=420,height=640');
  };
  document.addEventListener('DOMContentLoaded', function(){ document.body.appendChild(b); });
})();
