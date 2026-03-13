//src/utils/units.js
export const HECTARES_TO_ACRES = 2.47105;

export function toSize(valueInHa, unit = "ha") {
  if (valueInHa == null) return null;
  return unit === "ac"
    ? { value: parseFloat((valueInHa * HECTARES_TO_ACRES).toFixed(2)), unit: "ac" }
    : { value: parseFloat(valueInHa.toFixed(2)), unit: "ha" };
}
