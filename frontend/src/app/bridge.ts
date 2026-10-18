import {signal} from '@angular/core';
import {Streamlit} from 'streamlit-component-lib';
import {BridgePayload, emptyPayload} from './types';
export const payload = signal<BridgePayload>(emptyPayload);
let lastFingerprint = '';
export function connectStreamlit(): void {
  Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, (ev: Event) => {
    const event = ev as CustomEvent<{args?: {payload?: BridgePayload}}>;
    const next = event.detail?.args?.payload;
    if (next && Array.isArray(next.tabs)) {
      const fingerprint = JSON.stringify(next);
      if (fingerprint !== lastFingerprint) {
        lastFingerprint = fingerprint;
        payload.set(next);
      }
    }
    resizeFrame();
  });
  Streamlit.setComponentReady();
  resizeFrame();
}
export function resizeFrame(): void { requestAnimationFrame(() => Streamlit.setFrameHeight()); }
export function navigate(tab: string): void {
  // Navigation only: no data mutation is permitted from this PoC.
  const id = (typeof crypto !== 'undefined' && 'randomUUID' in crypto) ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(36).slice(2)}`;
  Streamlit.setComponentValue({type:'navigate',target:tab,id});
}
