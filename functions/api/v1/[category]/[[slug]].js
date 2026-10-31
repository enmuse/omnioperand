import { handleUniversalApiRequest, onRequestOptions } from '../_universal_solver_handler.js';

export { onRequestOptions };

export async function onRequestGet(context) {
  const category = context.params.category;
  const slug = context.params.slug;
  return handleUniversalApiRequest(context, category, slug);
}

export const onRequestHead = onRequestGet;

export async function onRequestPost(context) {
  const category = context.params.category;
  const slug = context.params.slug;
  return handleUniversalApiRequest(context, category, slug);
}
