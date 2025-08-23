export default [
    {
        files: ["**/*.js"],
        languageOptions: {
            ecmaVersion: 2022,
            sourceType: "script",
            globals: {
                // Browser globals
                document: "readonly",
                window: "readonly",
                console: "readonly",
                alert: "readonly",
                confirm: "readonly",
                setTimeout: "readonly",
                fetch: "readonly",
                URLSearchParams: "readonly",
                encodeURIComponent: "readonly",
                decodeURIComponent: "readonly",
                parseInt: "readonly"
            }
        },
        rules: {
            // Basic rules for clean code
            "no-unused-vars": "warn",
            "no-console": "off", // Allow console.log for debugging
            "semi": ["error", "always"],
            "quotes": ["error", "single", { "allowTemplateLiterals": true }],
            "no-var": "error",
            "prefer-const": "warn"
        }
    }
];