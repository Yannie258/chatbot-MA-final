export function normalizeUrl(url?: string): string {
    if (!url) return "#";
    return url.startsWith("http") ? url : `https://${url}`;
  }
  