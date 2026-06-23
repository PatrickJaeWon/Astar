"use strict";
(() => {
  var __getOwnPropNames = Object.getOwnPropertyNames;
  var __commonJS = (cb, mod) => function __require() {
    try {
      return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
    } catch (e) {
      throw mod = 0, e;
    }
  };
  var __async = (__this, __arguments, generator) => {
    return new Promise((resolve, reject) => {
      var fulfilled = (value) => {
        try {
          step(generator.next(value));
        } catch (e) {
          reject(e);
        }
      };
      var rejected = (value) => {
        try {
          step(generator.throw(value));
        } catch (e) {
          reject(e);
        }
      };
      var step = (x) => x.done ? resolve(x.value) : Promise.resolve(x.value).then(fulfilled, rejected);
      step((generator = generator.apply(__this, __arguments)).next());
    });
  };

  // src/code.ts
  var require_code = __commonJS({
    "src/code.ts"(exports) {
      figma.showUI(__html__, { width: 520, height: 700, title: "Claude HTML to Figma Design" });
      figma.ui.onmessage = (msg) => __async(null, null, function* () {
        if (msg.type === "import-html") {
          try {
            yield importElements(msg.elements, msg.canvasWidth, msg.canvasHeight);
            figma.ui.postMessage({ type: "success", message: "Design imported successfully!" });
          } catch (err) {
            figma.ui.postMessage({ type: "error", message: String(err) });
          }
        }
      });
      function importElements(elements, canvasWidth, canvasHeight) {
        return __async(this, null, function* () {
          const rootFrame = figma.createFrame();
          rootFrame.name = "Claude Design Import";
          rootFrame.resize(canvasWidth || 1440, canvasHeight || 900);
          rootFrame.fills = [{ type: "SOLID", color: { r: 1, g: 1, b: 1 } }];
          rootFrame.clipsContent = true;
          const viewport = figma.viewport.center;
          rootFrame.x = viewport.x - rootFrame.width / 2;
          rootFrame.y = viewport.y - rootFrame.height / 2;
          const scaleX = rootFrame.width / canvasWidth;
          const scaleY = rootFrame.height / canvasHeight;
          const scale = Math.min(scaleX, scaleY);
          for (const el of elements) {
            const node = yield createElement(el, scale);
            if (node) {
              rootFrame.appendChild(node);
            }
          }
          figma.currentPage.selection = [rootFrame];
          figma.viewport.scrollAndZoomIntoView([rootFrame]);
        });
      }
      function createElement(el, scale) {
        return __async(this, null, function* () {
          if (el.width < 1 || el.height < 1) return null;
          const hasText = el.text && el.text.trim().length > 0 && !el.children.length;
          const isImagePlaceholder = el.tagName === "IMG";
          if (hasText) {
            return yield createTextNode(el, scale);
          }
          const frame = figma.createFrame();
          frame.name = el.tagName.toLowerCase() + (el.id ? `#${el.id}` : "");
          frame.x = Math.round(el.x * scale);
          frame.y = Math.round(el.y * scale);
          frame.resize(Math.max(1, Math.round(el.width * scale)), Math.max(1, Math.round(el.height * scale)));
          frame.clipsContent = el.overflow === "hidden";
          frame.opacity = el.opacity;
          const bg = el.backgroundColor;
          if (bg.a > 0.01) {
            frame.fills = [{ type: "SOLID", color: { r: bg.r, g: bg.g, b: bg.b }, opacity: bg.a }];
          } else {
            frame.fills = [];
          }
          if (el.borderRadius > 0) {
            frame.cornerRadius = Math.round(el.borderRadius * scale);
          }
          if (el.borderWidth > 0 && el.borderColor.a > 0.01) {
            const bc = el.borderColor;
            frame.strokes = [{ type: "SOLID", color: { r: bc.r, g: bc.g, b: bc.b }, opacity: bc.a }];
            frame.strokeWeight = Math.max(1, Math.round(el.borderWidth * scale));
            frame.strokeAlign = "INSIDE";
          }
          if (el.boxShadow && el.boxShadow !== "none") {
            const shadow = parseShadow(el.boxShadow);
            if (shadow) {
              frame.effects = [shadow];
            }
          }
          if (el.imageData) {
            try {
              const base64 = el.imageData.replace(/^data:[^;]+;base64,/, "");
              const binaryStr = atob(base64);
              const bytes = new Uint8Array(binaryStr.length);
              for (let i = 0; i < binaryStr.length; i++) bytes[i] = binaryStr.charCodeAt(i);
              const img = figma.createImage(bytes);
              frame.fills = [{ type: "IMAGE", imageHash: img.hash, scaleMode: "FILL" }];
            } catch (_e) {
              if (isImagePlaceholder) {
                frame.fills = [{ type: "SOLID", color: { r: 0.85, g: 0.85, b: 0.85 } }];
              }
            }
          } else if (isImagePlaceholder) {
            frame.fills = [{ type: "SOLID", color: { r: 0.85, g: 0.85, b: 0.85 } }];
            frame.name = "img";
          }
          for (const child of el.children) {
            const childNode = yield createElement(child, scale);
            if (childNode) {
              frame.appendChild(childNode);
            }
          }
          if (!el.children.length && frame.fills && frame.fills.length === 0 && !frame.strokes.length) {
            frame.layoutMode = "NONE";
          }
          return frame;
        });
      }
      function createTextNode(el, scale) {
        return __async(this, null, function* () {
          if (!el.text) return null;
          try {
            yield figma.loadFontAsync({ family: "Inter", style: "Regular" });
            yield figma.loadFontAsync({ family: "Inter", style: "Bold" });
            const text = figma.createText();
            text.x = Math.round(el.x * scale);
            text.y = Math.round(el.y * scale);
            text.opacity = el.opacity;
            const fontStyle = resolveFontStyle(el.fontWeight, el.fontStyle);
            try {
              yield figma.loadFontAsync({ family: el.fontFamily, style: fontStyle });
              text.fontName = { family: el.fontFamily, style: fontStyle };
            } catch (e) {
              text.fontName = { family: "Inter", style: fontStyle === "Bold Italic" || fontStyle === "Italic" ? "Regular" : fontStyle };
            }
            text.fontSize = Math.max(1, Math.round(el.fontSize * scale));
            text.characters = el.text.trim();
            const col = el.color;
            text.fills = [{ type: "SOLID", color: { r: col.r, g: col.g, b: col.b }, opacity: col.a }];
            if (el.letterSpacing > 0) {
              text.letterSpacing = { value: el.letterSpacing * scale, unit: "PIXELS" };
            }
            if (el.lineHeight > 0) {
              text.lineHeight = { value: el.lineHeight * scale, unit: "PIXELS" };
            }
            switch (el.textAlign) {
              case "center":
                text.textAlignHorizontal = "CENTER";
                break;
              case "right":
                text.textAlignHorizontal = "RIGHT";
                break;
              case "justify":
                text.textAlignHorizontal = "JUSTIFIED";
                break;
              default:
                text.textAlignHorizontal = "LEFT";
            }
            if (el.textDecoration === "underline") {
              text.textDecoration = "UNDERLINE";
            } else if (el.textDecoration === "line-through") {
              text.textDecoration = "STRIKETHROUGH";
            }
            text.textAutoResize = "HEIGHT";
            text.resize(Math.max(1, Math.round(el.width * scale)), text.height);
            return text;
          } catch (err) {
            console.error("Failed to create text node:", err);
            return null;
          }
        });
      }
      function resolveFontStyle(weight, style) {
        const w = parseInt(weight) || 400;
        const isBold = w >= 600;
        const isItalic = style === "italic" || style === "oblique";
        if (isBold && isItalic) return "Bold Italic";
        if (isBold) return "Bold";
        if (isItalic) return "Italic";
        if (w >= 500) return "Medium";
        return "Regular";
      }
      function parseShadow(shadowStr) {
        const match = shadowStr.match(
          /(-?\d+(?:\.\d+)?px)\s+(-?\d+(?:\.\d+)?px)\s+(-?\d+(?:\.\d+)?px)(?:\s+(-?\d+(?:\.\d+)?px))?\s+(rgba?\([^)]+\)|#[0-9a-fA-F]+|\w+)/
        );
        if (!match) return null;
        const ox = parseFloat(match[1]);
        const oy = parseFloat(match[2]);
        const blur = parseFloat(match[3]);
        const color = parseColor(match[5] || "rgba(0,0,0,0.25)");
        return {
          type: "DROP_SHADOW",
          color: { r: color.r, g: color.g, b: color.b, a: color.a },
          offset: { x: ox, y: oy },
          radius: blur,
          spread: 0,
          visible: true,
          blendMode: "NORMAL"
        };
      }
      function parseColor(colorStr) {
        const rgbaMatch = colorStr.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)/);
        if (rgbaMatch) {
          return {
            r: parseInt(rgbaMatch[1]) / 255,
            g: parseInt(rgbaMatch[2]) / 255,
            b: parseInt(rgbaMatch[3]) / 255,
            a: rgbaMatch[4] !== void 0 ? parseFloat(rgbaMatch[4]) : 1
          };
        }
        return { r: 0, g: 0, b: 0, a: 0.25 };
      }
    }
  });
  require_code();
})();
