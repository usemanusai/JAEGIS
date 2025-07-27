/**
 * Jest Configuration for JAEGIS AI System
 * Comprehensive testing setup with mocking for Redis and OpenRouter APIs
 */

module.exports = {
  // Test environment
  testEnvironment: 'node',
  
  // Test file patterns
  testMatch: [
    '**/tests/**/*.test.js',
    '**/src/**/*.test.js',
    '**/__tests__/**/*.js'
  ],
  
  // Setup files
  setupFilesAfterEnv: [
    '<rootDir>/tests/setup.js'
  ],
  
  // Module paths
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/src/',
    '^@ai/(.*)$': '<rootDir>/src/nodejs/ai/',
    '^@tests/(.*)$': '<rootDir>/tests/'
  },
  
  // Coverage configuration
  collectCoverage: true,
  collectCoverageFrom: [
    'src/nodejs/ai/**/*.js',
    'src/nodejs/**/*.js',
    '!src/nodejs/**/*.test.js',
    '!src/nodejs/test/**',
    '!**/node_modules/**',
    '!**/coverage/**',
    '!**/dist/**'
  ],
  
  // Coverage thresholds (90%+ requirement)
  coverageThreshold: {
    global: {
      branches: 90,
      functions: 90,
      lines: 90,
      statements: 90
    }
  },
  
  // Coverage reporters
  coverageReporters: [
    'text',
    'text-summary',
    'lcov',
    'html',
    'json'
  ],
  
  // Coverage directory
  coverageDirectory: 'coverage',
  
  // Test timeout (30 seconds for AI operations)
  testTimeout: 30000,
  
  // Clear mocks between tests
  clearMocks: true,
  restoreMocks: true,
  resetMocks: true,
  
  // Verbose output
  verbose: true
};
