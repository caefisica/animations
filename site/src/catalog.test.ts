import { describe, expect, it } from "vitest";
import { catalog, findAnimation, mediaUrl } from "./catalog";

describe("catalog", () => {
  it("has unique slugs", () => {
    const slugs = catalog.map((item) => item.slug);
    expect(new Set(slugs).size).toBe(slugs.length);
  });

  it("finds an animation by slug", () => {
    expect(findAnimation("drude")?.title).toContain("Drude");
    expect(findAnimation("missing")).toBeUndefined();
  });

  it("builds media urls under the base path", () => {
    expect(mediaUrl("drude.mp4", "/animations/")).toBe("/animations/media/drude.mp4");
  });
});
