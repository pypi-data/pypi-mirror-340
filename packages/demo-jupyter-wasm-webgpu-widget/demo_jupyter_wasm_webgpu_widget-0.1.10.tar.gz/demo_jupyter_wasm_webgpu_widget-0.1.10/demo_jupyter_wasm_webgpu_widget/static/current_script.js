// ts/current_script.js
Object.defineProperty(document, "currentScript", {
  get: function() {
    return {
      src: "widget.js",
      tagName: "script"
    };
  }
});
