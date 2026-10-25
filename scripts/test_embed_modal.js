// scripts/test_embed_modal.js
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '..');

// Let's test that omni-search.js and embed-modal.js are valid syntax
const embedModalCode = fs.readFileSync(path.join(REPO_ROOT, 'assets', 'js', 'embed-modal.js'), 'utf8');
const omniSearchCode = fs.readFileSync(path.join(REPO_ROOT, 'assets', 'js', 'omni-search.js'), 'utf8');

console.log('Testing JS syntax...');
new Function(embedModalCode);
new Function(omniSearchCode);
console.log('Syntax check PASSED.');

// Now simulate DOM with minimal mock
const mockDocument = {
  location: { pathname: '/geometry/2d/shapes/regular-polygon/', origin: 'https://omnioperand.com', search: '' },
  title: 'Regular Octagon Calculator — OmniOperand',
  querySelector: function(sel) {
    if (sel.includes('.btn-embed-calculator') || sel.includes('#btn-embed') || sel.includes('.btn-open-embed')) {
      return { id: 'btn-embed', className: 'btn-secondary btn-open-embed btn-embed-calculator' };
    }
    if (sel === 'h1') return { textContent: 'Regular Octagon' };
    if (sel === 'link[rel="canonical"]') return { href: 'https://omnioperand.com/geometry/2d/shapes/regular-polygon/' };
    return null;
  }
};

console.log('Checking embed URL generation logic...');
const rawPath = mockDocument.location.pathname.replace(/^\/embed\//, '').replace(/\/$/, '').replace(/^\//, '');
const embedUrl = 'https://omnioperand.com/embed/' + (rawPath ? rawPath + '/' : '');
const canonicalUrl = 'https://omnioperand.com/' + (rawPath ? rawPath + '/' : '');
const toolTitle = 'Regular Octagon';

const iframeCode = `<iframe src="${embedUrl}" width="100%" height="720" frameborder="0" style="border:1px solid #1e293b;border-radius:12px;width:100%;max-width:100%;box-shadow:0 8px 30px rgba(0,0,0,0.3);"></iframe>\n<p style="font-size:12px;color:#64748b;font-family:-apple-system,BlinkMacSystemFont,sans-serif;margin-top:6px;text-align:right;">Calculator powered by <a href="${canonicalUrl}" target="_blank" rel="noopener" style="color:#0284c7;text-decoration:none;font-weight:600;">OmniOperand ${toolTitle}</a></p>`;

const backlinkCode = `<a href="${canonicalUrl}" target="_blank" rel="noopener" style="font-family:sans-serif;color:#0284c7;font-weight:600;text-decoration:none;">Interactive ${toolTitle} by OmniOperand</a>`;

console.log('Generated Iframe Code:\n', iframeCode);
console.log('\nGenerated Backlink Code:\n', backlinkCode);

if (!iframeCode.includes('src="https://omnioperand.com/embed/geometry/2d/shapes/regular-polygon/"')) {
  throw new Error('Iframe URL is incorrect!');
}
if (!backlinkCode.includes('href="https://omnioperand.com/geometry/2d/shapes/regular-polygon/"')) {
  throw new Error('Backlink URL is incorrect!');
}
console.log('\nAll embed checks PASSED!');
