import eslint from "@eslint/js";
import tseslint from "typescript-eslint";

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  {
    ignores: [
      "**/node_modules/**",
      "**/.venv/**",
      "**/.next/**",
      "**/dist/**",
      "**/build/**",
      "**/coverage/**",
      "**/.git/**",
    ],
  },
  {
    files: [
      "typescript/**/*.ts",
      "repos/VeriFi/frontend/src/**/*.{ts,tsx}",
      "repos/Lens/frontend/**/*.{ts,tsx}",
      "repos/SlugSync/supabase/functions/**/*.ts",
    ],
  }
);
