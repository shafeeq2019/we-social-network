import stylistic from '@stylistic/eslint-plugin';
import tseslint from 'typescript-eslint';

const baseConfig = {
  name: 'baseConfig',
  plugins: {
    '@stylistic': stylistic
  },
  languageOptions: {
    parserOptions: {
      parser: tseslint.parser,
    }
  },
  rules: {
    'quotes': ['error', 'single'],
    'object-shorthand': 'error',
    'semi': ['error', 'always'],
    'prefer-const': 'error',
    'no-trailing-spaces': 'error',
    'keyword-spacing': 'error',
    'no-multiple-empty-lines': ['error', { 'max': 1, }],
    '@stylistic/indent': [
      'error',
      2
    ],
    '@stylistic/array-bracket-spacing': 'error',
    '@stylistic/member-delimiter-style': 'error',
    '@stylistic/key-spacing': 'error',
    '@stylistic/keyword-spacing': 'error',
    '@stylistic/no-multi-spaces': 'error',
    '@stylistic/object-property-newline': ['error', {
      allowAllPropertiesOnSameLine: true
    }],
    '@stylistic/brace-style': ['error', '1tbs'],
    '@stylistic/comma-spacing': ['error', {
      before: false,
      after: true
    }],
    '@stylistic/object-curly-spacing': ['error', 'always'],
  }
};

const vueConfig = {
  name: 'vueConfig',
  files: ['**/*.{ts,vue}'],

  rules: {
    'vue/require-v-for-key': 'error',
    'vue/no-unused-vars': 'error',
    'vue/no-parsing-error': 'error',
    'vue/multi-word-component-names': 'off',
    'vue/html-indent': ['error', 2, {
      'attribute': 1,
      'baseIndent': 1,
      'closeBracket': 1,
      'alignAttributesVertically': true,
      'ignores': []
    }],
    'vue/no-multi-spaces': ['error', {
      'ignoreProperties': false
    }],
    'vue/padding-line-between-blocks': 'error'
  }
};

export {
  baseConfig,
  vueConfig,
};
