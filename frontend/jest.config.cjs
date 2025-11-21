/** @type {import('jest').Config} */
const config = {
  testEnvironment: "jsdom",
  moduleFileExtensions: ["ts", "tsx", "js", "jsx"],
  testMatch: ["**/__tests__/**/*.(test|spec).[jt]s?(x)"],
  transform: {
    "^.+\\.(t|j)sx?$": "babel-jest",
  },
  moduleNameMapper: {
    "^@/(.*)$": "<rootDir>/$1",
    "^next/link$": "<rootDir>/test/__mocks__/nextLinkMock.tsx",
    "^next/font/google$": "<rootDir>/test/__mocks__/nextFontMock.js",
    "^.+\\.(css|less|scss|sass)$": "<rootDir>/test/__mocks__/styleMock.js",
  },
  setupFilesAfterEnv: ["<rootDir>/test/setupTests.ts"],
};

module.exports = config;