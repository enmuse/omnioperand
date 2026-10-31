import { handleUniversalApiRequest, onRequestOptions } from '../_universal_solver_handler.js';

export { onRequestOptions };

export async function onRequestGet(context) {
  const slug = context.params.slug;
  return handleUniversalApiRequest(context, 'finance', slug);
}

export const onRequestHead = onRequestGet;

export async function onRequestPost(context) {
  const slug = context.params.slug;
  return handleUniversalApiRequest(context, 'finance', slug);
}
