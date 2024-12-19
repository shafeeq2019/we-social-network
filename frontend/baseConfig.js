import stylistic from "@stylistic/eslint-plugin";
import tseslint from "typescript-eslint";

const baseConfig = {
  name: "baseConfig",
  plugins: {
    "@stylistic": stylistic
  },
  rules: {
    "object-shorthand": "error",
    "semi": ["error", "always"],
    "prefer-const": "error",
    "no-trailing-spaces": "error",
    "keyword-spacing": "error",
    "@stylistic/indent": [
      "error",
      2
    ],
    "@stylistic/array-bracket-spacing": "error",
    "@stylistic/member-delimiter-style": "error",
    "@stylistic/key-spacing": "error",
    "@stylistic/keyword-spacing": "error",
    "@stylistic/no-multi-spaces": "error",
    "@stylistic/object-property-newline": ["error", {
      allowAllPropertiesOnSameLine: true
    }],
    "@stylistic/brace-style": ["error", "1tbs"],
    "@stylistic/comma-spacing": ["error", {
      before: false,
      after: true
    }],
  }
};

const vueConfig = {
  name: "vueConfig",
  files: ["**/*.vue"],
  languageOptions: {
    parserOptions: {
      parser: tseslint.parser
    }
  },
  rules: {
    "vue/multi-word-component-names": "off",
    "vue/html-indent": ["error", 2, {
      "attribute": 1,
      "baseIndent": 1,
      "closeBracket": 1,
      "alignAttributesVertically": true,
      "ignores": []
    }],
    "vue/no-multi-spaces": ["error", {
      "ignoreProperties": false
    }]
  }
};

export {
  baseConfig,
  vueConfig
};
