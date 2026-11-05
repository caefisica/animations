import { defineConfig } from "vitest/config";
import solid from "@solidjs/vite-plugin";

export default defineConfig({
  base: "/animations/",
  plugins: [solid()],
  test: { environment: "node" },
});
