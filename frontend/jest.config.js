module.exports = {
    roots: ['<rootDir>/src', '<rootDir>/tests'],
    testRegex: '(/__tests__/.*|(\\.|/)(test|spec))\\.jsx?$',
    moduleFileExtensions: ['js', 'jsx', 'json'],
    testEnvironment: 'jest-environment-jsdom',
    collectCoverage: true,
    coverageReporters: ['json', 'lcov', 'text', 'clover'],
    collectCoverageFrom: [
      'src/**/*.{js,jsx}',
      '!src/index.js',
    ],
  };
  