const test = require("node:test");
const assert = require("node:assert/strict");

const {
  matchesDifficultyFilter,
  getNextDifficultySelection,
} = require("../src/static/app.js");

test("matchesDifficultyFilter applies level and unspecified rules", () => {
  assert.equal(matchesDifficultyFilter({ difficulty: "Beginner" }, "Beginner"), true);
  assert.equal(matchesDifficultyFilter({ difficulty: "Intermediate" }, "Beginner"), false);
  assert.equal(matchesDifficultyFilter({ description: "No difficulty" }, "unspecified"), true);
  assert.equal(matchesDifficultyFilter({ difficulty: "Advanced" }, "unspecified"), false);
  assert.equal(matchesDifficultyFilter({ difficulty: "" }, "unspecified"), false);
  assert.equal(matchesDifficultyFilter({ difficulty: "Advanced" }, null), true);
});

test("getNextDifficultySelection toggles active selection off on second click", () => {
  assert.equal(getNextDifficultySelection(null, "Beginner"), "Beginner");
  assert.equal(getNextDifficultySelection("Beginner", "Beginner"), null);
  assert.equal(getNextDifficultySelection("Beginner", "Advanced"), "Advanced");
});
