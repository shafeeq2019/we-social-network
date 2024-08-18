import stylistic from "@stylistic/eslint-plugin";

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
  rules: {
    "vue/multi-word-component-names": "off"
  }
};

export {
  baseConfig,
  vueConfig
};
