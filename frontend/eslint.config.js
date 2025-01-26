import globals from 'globals';
import pluginJs from '@eslint/js';
import tseslint from 'typescript-eslint';
import pluginVue from 'eslint-plugin-vue';
import { baseConfig, vueConfig } from './baseConfig.js';

/** @type {import('eslint').Linter.Config[]} */
export default [
  {
    files: ['**/*.{js,mjs,cjs,ts,vue}']
  },
  {
    languageOptions: { globals: globals.browser }
  },
  {
    ignores: [
      'node_modules',
      'public',
      'dist',
      'index.html'
    ]
  },

  pluginJs.configs.recommended,
  ...tseslint.configs.recommended,
  ...pluginVue.configs['flat/essential'],
  baseConfig,
  vueConfig
];

