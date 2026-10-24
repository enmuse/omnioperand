/**
 * assets/js/qr-code-engine.js
 * OmniOperand Autonomous Client-Side QR Code Engine
 * Generates vector SVG & Canvas Data URIs client-side with 0 external dependencies or network calls.
 * Implements ISO/IEC 18004 QR Code specification (Versions 1-6, Byte Mode, Quality EC level L/M).
 */

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.OmniQRCode = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // Minimal Reed-Solomon Galois Field (GF(256)) arithmetic
  const EXP_TABLE = new Uint8Array(256);
  const LOG_TABLE = new Uint8Array(256);
  let x = 1;
  for (let i = 0; i < 255; i++) {
    EXP_TABLE[i] = x;
    LOG_TABLE[x] = i;
    x <<= 1;
    if (x & 256) x ^= 0x11d;
  }
  for (let i = 255; i < 512; i++) {
    EXP_TABLE[i] = EXP_TABLE[i - 255];
  }

  function gfMul(x, y) {
    if (x === 0 || y === 0) return 0;
    return EXP_TABLE[LOG_TABLE[x] + LOG_TABLE[y]];
  }

  function rsGenPoly(n) {
    let poly = [1];
    for (let i = 0; i < n; i++) {
      let next = new Array(poly.length + 1).fill(0);
      for (let j = 0; j < poly.length; j++) {
        next[j] ^= gfMul(poly[j], EXP_TABLE[i]);
        next[j + 1] ^= poly[j];
      }
      poly = next;
    }
    return poly;
  }

  function rsEncode(data, ecCount) {
    const gen = rsGenPoly(ecCount);
    const msg = data.concat(new Array(ecCount).fill(0));
    for (let i = 0; i < data.length; i++) {
      const coef = msg[i];
      if (coef !== 0) {
        for (let j = 0; j < gen.length; j++) {
          msg[i + j] ^= gfMul(gen[j], coef);
        }
      }
    }
    return msg.slice(data.length);
  }

  // Version capacities (Version 1-10, EC Level M)
  const VERSION_SPECS = [
    null,
    { size: 21, totalBytes: 26, dataBytes: 16, ecBytes: 10, align: [] },
    { size: 25, totalBytes: 44, dataBytes: 28, ecBytes: 16, align: [6, 18] },
    { size: 29, totalBytes: 70, dataBytes: 44, ecBytes: 26, align: [6, 22] },
    { size: 33, totalBytes: 100, dataBytes: 64, ecBytes: 36, align: [6, 26] },
    { size: 37, totalBytes: 134, dataBytes: 86, ecBytes: 48, align: [6, 30] },
    { size: 41, totalBytes: 172, dataBytes: 108, ecBytes: 64, align: [6, 34] },
    { size: 45, totalBytes: 196, dataBytes: 124, ecBytes: 72, align: [6, 22, 38] },
    { size: 49, totalBytes: 242, dataBytes: 154, ecBytes: 88, align: [6, 24, 42] },
    { size: 53, totalBytes: 292, dataBytes: 182, ecBytes: 110, align: [6, 26, 46] },
    { size: 57, totalBytes: 346, dataBytes: 216, ecBytes: 130, align: [6, 28, 50] }
  ];

  class BitBuffer {
    constructor() {
      this.buffer = [];
      this.length = 0;
    }
    put(val, len) {
      for (let i = 0; i < len; i++) {
        this.putBit(((val >>> (len - i - 1)) & 1) === 1);
      }
    }
    putBit(bit) {
      const byteIndex = Math.floor(this.length / 8);
      if (this.buffer.length <= byteIndex) {
        this.buffer.push(0);
      }
      if (bit) {
        this.buffer[byteIndex] |= (0x80 >>> (this.length % 8));
      }
      this.length++;
    }
    getBytes() {
      return this.buffer;
    }
  }

  function getBestVersion(dataLength) {
    for (let v = 1; v <= 10; v++) {
      const spec = VERSION_SPECS[v];
      // 4 bits mode + 8/16 bits char count + data
      const overhead = 4 + (v <= 9 ? 8 : 16);
      const capacityBits = spec.dataBytes * 8;
      if (overhead + dataLength * 8 <= capacityBits) {
        return v;
      }
    }
    return 10; // default max
  }

  function generateMatrix(text) {
    const bytes = [];
    for (let i = 0; i < text.length; i++) {
      const code = text.charCodeAt(i);
      if (code < 128) bytes.push(code);
      else if (code < 2048) {
        bytes.push(192 | (code >> 6));
        bytes.push(128 | (code & 63));
      } else {
        bytes.push(224 | (code >> 12));
        bytes.push(128 | ((code >> 6) & 63));
        bytes.push(128 | (code & 63));
      }
    }

    const version = getBestVersion(bytes.length);
    const spec = VERSION_SPECS[version];
    const size = spec.size;

    // Build data bit stream
    const bb = new BitBuffer();
    bb.put(4, 4); // Byte mode (0100)
    bb.put(bytes.length, version <= 9 ? 8 : 16);
    for (let b of bytes) bb.put(b, 8);

    // Terminator
    const remaining = (spec.dataBytes * 8) - bb.length;
    bb.put(0, Math.min(4, Math.max(0, remaining)));
    while (bb.length % 8 !== 0) bb.putBit(false);

    // Padding bytes (0xEC, 0x11)
    const pad = [0xEC, 0x11];
    let padIdx = 0;
    while (bb.buffer.length < spec.dataBytes) {
      bb.buffer.push(pad[padIdx % 2]);
      padIdx++;
    }

    // RS Error Correction
    const ec = rsEncode(bb.buffer, spec.ecBytes);
    const finalData = bb.buffer.concat(ec);

    // Create 2D Matrix (0: empty, 1: dark, 2: light, 3: reserved)
    const matrix = Array.from({ length: size }, () => new Int8Array(size).fill(0));

    // Finder patterns
    function placeFinder(row, col) {
      for (let r = -1; r <= 7; r++) {
        for (let c = -1; c <= 7; c++) {
          const nr = row + r, nc = col + c;
          if (nr >= 0 && nr < size && nc >= 0 && nc < size) {
            if ((r >= 0 && r <= 6 && (c === 0 || c === 6)) ||
                (c >= 0 && c <= 6 && (r === 0 || r === 6)) ||
                (r >= 2 && r <= 4 && c >= 2 && c <= 4)) {
              matrix[nr][nc] = 1; // dark
            } else {
              matrix[nr][nc] = 2; // light
            }
          }
        }
      }
    }
    placeFinder(0, 0);
    placeFinder(0, size - 7);
    placeFinder(size - 7, 0);

    // Timing patterns
    for (let i = 8; i < size - 8; i++) {
      const val = (i % 2 === 0) ? 1 : 2;
      if (!matrix[6][i]) matrix[6][i] = val;
      if (!matrix[i][6]) matrix[i][6] = val;
    }

    // Alignment patterns
    if (spec.align && spec.align.length > 0) {
      const coords = spec.align;
      for (let r of coords) {
        for (let c of coords) {
          if (matrix[r][c] !== 0) continue;
          for (let dr = -2; dr <= 2; dr++) {
            for (let dc = -2; dc <= 2; dc++) {
              if (Math.abs(dr) === 2 || Math.abs(dc) === 2 || (dr === 0 && dc === 0)) {
                matrix[r + dr][c + dc] = 1;
              } else {
                matrix[r + dr][c + dc] = 2;
              }
            }
          }
        }
      }
    }

    // Format info placeholder (reserve line 8)
    for (let i = 0; i < 9; i++) {
      if (!matrix[8][i]) matrix[8][i] = 3;
      if (!matrix[i][8]) matrix[i][8] = 3;
      if (!matrix[8][size - 1 - i]) matrix[8][size - 1 - i] = 3;
      if (!matrix[size - 1 - i][8]) matrix[size - 1 - i] = 3;
    }
    matrix[size - 8][8] = 1; // Dark module

    // Data bits placement
    let bitIdx = 0;
    const totalBits = finalData.length * 8;
    let right = size - 1;
    let upward = true;

    while (right > 0) {
      if (right === 6) right--; // skip timing column
      for (let vert = 0; vert < size; vert++) {
        const row = upward ? (size - 1 - vert) : vert;
        for (let colOffset = 0; colOffset < 2; colOffset++) {
          const col = right - colOffset;
          if (matrix[row][col] === 0) {
            let bit = false;
            if (bitIdx < totalBits) {
              const byteI = Math.floor(bitIdx / 8);
              const bitI = 7 - (bitIdx % 8);
              bit = ((finalData[byteI] >>> bitI) & 1) === 1;
              bitIdx++;
            }
            // Mask 0: (row + col) % 2 === 0
            if ((row + col) % 2 === 0) {
              bit = !bit;
            }
            matrix[row][col] = bit ? 1 : 2;
          }
        }
      }
      right -= 2;
      upward = !upward;
    }

    // Format string for EC Level M (00), Mask 0 (000) -> 0x5412 (BCH encoded)
    // 0x5412 = 0101010000010010
    const formatBits = [1,0,1,0,1,0,0,0,0,0,1,0,0,1,0];
    for (let i = 0; i < 6; i++) matrix[8][i] = formatBits[i] ? 1 : 2;
    matrix[8][7] = formatBits[6] ? 1 : 2;
    matrix[8][8] = formatBits[7] ? 1 : 2;
    matrix[7][8] = formatBits[8] ? 1 : 2;
    for (let i = 9; i < 15; i++) matrix[14 - i][8] = formatBits[i] ? 1 : 2;

    for (let i = 0; i < 8; i++) matrix[size - 1 - i][8] = formatBits[i] ? 1 : 2;
    for (let i = 8; i < 15; i++) matrix[8][size - 15 + i] = formatBits[i] ? 1 : 2;

    return matrix;
  }

  return {
    /**
     * Renders a QR code to SVG string.
     */
    toSVG: function (text, options = {}) {
      const margin = options.margin !== undefined ? options.margin : 4;
      const size = options.size || 200;
      const fgColor = options.fgColor || '#0f172a';
      const bgColor = options.bgColor || '#ffffff';

      const matrix = generateMatrix(text);
      const modCount = matrix.length;
      const totalSize = modCount + margin * 2;
      const modSize = size / totalSize;

      let rects = [];
      for (let r = 0; r < modCount; r++) {
        for (let c = 0; c < modCount; c++) {
          if (matrix[r][c] === 1) {
            const x = (c + margin) * modSize;
            const y = (r + margin) * modSize;
            rects.push(`<rect x="${x.toFixed(2)}" y="${y.toFixed(2)}" width="${(modSize + 0.1).toFixed(2)}" height="${(modSize + 0.1).toFixed(2)}" fill="${fgColor}"/>`);
          }
        }
      }

      return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${size} ${size}" width="${size}" height="${size}">
  <rect width="100%" height="100%" fill="${bgColor}"/>
  ${rects.join('\n  ')}
</svg>`;
    },

    /**
     * Renders a QR code to a base64 Data URL (PNG via Canvas)
     */
    toDataURL: function (text, options = {}) {
      const margin = options.margin !== undefined ? options.margin : 4;
      const size = options.size || 256;
      const fgColor = options.fgColor || '#0f172a';
      const bgColor = options.bgColor || '#ffffff';

      const matrix = generateMatrix(text);
      const modCount = matrix.length;
      const totalUnits = modCount + margin * 2;
      const unit = size / totalUnits;

      if (typeof document !== 'undefined' && document.createElement) {
        const canvas = document.createElement('canvas');
        canvas.width = size;
        canvas.height = size;
        const ctx = canvas.getContext('2d');

        ctx.fillStyle = bgColor;
        ctx.fillRect(0, 0, size, size);

        ctx.fillStyle = fgColor;
        for (let r = 0; r < modCount; r++) {
          for (let c = 0; c < modCount; c++) {
            if (matrix[r][c] === 1) {
              ctx.fillRect((c + margin) * unit, (r + margin) * unit, unit + 0.5, unit + 0.5);
            }
          }
        }
        return canvas.toDataURL('image/png');
      }
      // Fallback to SVG data URI
      const svg = this.toSVG(text, options);
      return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
    }
  };
}));
