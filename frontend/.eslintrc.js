module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    "plugin:vue/vue3-essential",
    "eslint:recommended",
    "@vue/typescript/recommended",
    "@vue/prettier",
    "@vue/prettier/@typescript-eslint",
  ],
  parserOptions: {
    ecmaVersion: 2020,
  },
  rules: {
    "no-console": process.env.NODE_ENV === "production" ? "warn" : "off",
    "no-debugger": process.env.NODE_ENV === "production" ? "warn" : "off",
    "no-var-requires": "off",
    "prettier/prettier": [
      "error",
      {
        singleQuote: true,
        endOfLine: "auto",
        semi: false,
        tabWidth: 2,
        trailingComma: "es5",
        bracketSpacing: true,
      }
    ],
  },
};
