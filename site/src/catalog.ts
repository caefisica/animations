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
    seconds: 28,
  },
  {
    slug: "classical-failure",
    title: "La falla clásica",
    topic: "Física del estado sólido",
    summary:
      "Drude predice C = 3R/2 = 12,5 J/(mol K) para los electrones del cobre. A 300 K se mide 0,21: unas 60 veces menos.",
    video: "classical-failure.mp4",
    poster: "classical-failure.png",
    seconds: 18,
  },
  {
    slug: "sommerfeld",
    title: "Sommerfeld: ondas en una caja",
    topic: "Física del estado sólido",
    summary:
      "Los electrones llenan los estados k de menor energía, dos por punto (Pauli), hasta la esfera de Fermi. En el cobre E_F = 7,0 eV.",
    video: "sommerfeld.mp4",
    poster: "sommerfeld.png",
    seconds: 14,
  },
];

export function mediaUrl(file: string, base: string = import.meta.env.BASE_URL): string {
  return `${base}media/${file}`;
}

export function findAnimation(slug: string): Animation | undefined {
  return catalog.find((item) => item.slug === slug);
}
