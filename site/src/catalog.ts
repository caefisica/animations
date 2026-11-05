export interface Animation {
  slug: string;
  title: string;
  topic: string;
  summary: string;
  /** File names under public/media, without the base path. */
  video: string;
  poster: string;
  seconds: number;
}

export const catalog: Animation[] = [
  {
    slug: "drude",
    title: "Drude: la conductividad",
    topic: "Electromagnetismo",
    summary:
      "Electrones libres chocan con una red de iones. El campo E los empuja y la resistividad sale de ρ = m / (n e² τ).",
    video: "drude.mp4",
    poster: "drude.png",
    seconds: 5,
  },
];

export function mediaUrl(file: string, base: string = import.meta.env.BASE_URL): string {
  return `${base}media/${file}`;
}

export function findAnimation(slug: string): Animation | undefined {
  return catalog.find((item) => item.slug === slug);
}
