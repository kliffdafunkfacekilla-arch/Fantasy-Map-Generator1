1. Add "type" to the Good interface, where the type is "raw" or "manufactured".
2. Update GOODS_DATA to have the "type" parameter on every single good.
   - For goods with recipes, they should be "manufactured" (or maybe both, but in the previous code it checks if recipes are empty. If recipes exist, it's manufactured, otherwise it's raw). Let me double-check the controller code.
   - Wait, `good-editor.ts` says: `a good is either gathered (raw) or made from recipes (manufactured)`
     - if recipes.length > 0 && !isRawProductionEmpty() -> ?? (maybe can be both, but typically it is one or the other).
   - "Missing detailed goods catalogs, production resource inputs, and specific raw vs manufactured tags"
     - Ah, "specific raw vs manufactured tags". It says "tags: string[]", so we just need to append "raw" or "manufactured" to the `tags` array!
3. Re-read: "Migrate detailed goods catalogs, production resource inputs, and specific raw vs manufactured tags into goods-generator.ts"
   - Is it just adding "raw" or "manufactured" to the `tags` array of each good?
   - "production resource inputs" -> In original legacy `src/generators/goods-generator.ts`, does it have `recipes`?
   - Oh, I compared `src/generators/goods-generator.ts` and `fmg-rebuild/simulation/civilization/goods-generator.ts` and they both have `recipes`.
   - Wait, the issue says "into goods-generator.ts". Which one? `fmg-rebuild/simulation/civilization/goods-generator.ts`! Because it says "Missing detailed goods catalogs, production resource inputs, and specific raw vs manufactured tags." in `fmg-rebuild/AUDIT_REPORT.md`.
   - Let's check `fmg-rebuild/simulation/civilization/goods-generator.ts`.
