# Testing Documentation

### Contents
1. [HTML Validation](#html-validation)
2. [CSS Validation](#css-validation)
3. [JavaScript Validation](#javascript-validation)
4. [Python Code Quality](#python-code-quality)
5. [Lighthouse Performance Testing](#lighthouse-performance-testing)

## HTML Validation

All pages tested using [W3C Markup Validator](https://validator.w3.org/).

| Page | URL | Status | Screenshot | Validation Link | Notes |
|------|-----|--------|------------|----------------|-------|
| [Home Welcome Landing Page](https://modmixx-427f89e87a1b.herokuapp.com/) | `/` | ✅ | ![home validation screenshot](docs/images/test-screenshots/home-html-validation.png) | [Home Result](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Fmodmixx-427f89e87a1b.herokuapp.com%2F) | Trailing slashes on void elements removed for validation. |
| [Sign Up Page](https://modmixx-427f89e87a1b.herokuapp.com/signup/) | `/signup/` | ✅ | ![sign up validation screenshot](docs/images/test-screenshots/sign-up-html-validation.png) | [Sign Up Result](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Fmodmixx-427f89e87a1b.herokuapp.com%2Fsignup%2F) |  |
| [Contact Page](https://modmixx-427f89e87a1b.herokuapp.com/contact/) | `/contact/` | ✅ | ![contact validation screenshot](docs/images/test-screenshots/contact-html-validation.png) | [Contact Result](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Fmodmixx-427f89e87a1b.herokuapp.com%2Fcontact%2F) |  |
| [About Page](https://modmixx-427f89e87a1b.herokuapp.com/about/) | `/about/` | ✅ | ![about validation screenshot](docs/images/test-screenshots/about-html-validation.png) | [About Result](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Fmodmixx-427f89e87a1b.herokuapp.com%2Fabout%2F) |  |
| [Login Page](https://modmixx-427f89e87a1b.herokuapp.com/login/) | `/login/` | ✅ | ![login validation screenshot](docs/images/test-screenshots/login-html-validation.png) | [Login Result](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Fmodmixx-427f89e87a1b.herokuapp.com%2Faccounts%2Flogin%2F) |  |
| [Third Party Login Page](https://modmixx-427f89e87a1b.herokuapp.com/google/login/) | `/google/login/` | ✅ | ![Google login validation screenshot](docs/images/test-screenshots/google-login-html-validation.png) | [Third Party Login Result](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Fmodmixx-427f89e87a1b.herokuapp.com%2Fgoogle%2Flogin%2F) |  |
| [Profile Set Up Page](https://modmixx-427f89e87a1b.herokuapp.com/profile/setup/) _login required_ | `/profile/setup/` | ✅  | ![Profile Set Up validation screenshot](docs/images/test-screenshots/profile-setup-html-validation.png) | Login required - validated by copying page source into the W3C validator’s “Validate by Direct Input” option. |  |
| [Profile Page](https://modmixx-427f89e87a1b.herokuapp.com/profile/jools/) _login required_ | `/profile/jools/` | ✅ | ![Profile validation screenshot](docs/images/test-screenshots/profile-html-validation.png) | Login required - validated by copying page source into the W3C validator’s “Validate by Direct Input” option. | Example profile username url. Fixed: removed controlslist attribute for mvp (future plans to build custom audio player) ![audio controls error screenshot](docs/images/test-screenshots/controls-list-error-html-validation.png) |
| [Profile Edit Page](https://modmixx-427f89e87a1b.herokuapp.com/profile/edit/) _login required_ | `/profile/edit/` | ✅ |![Profile Edit validation screenshot](docs/images/test-screenshots/profile-edit-html-validation.png) | Login required - validated by copying page source into the W3C validator’s “Validate by Direct Input” option.   |
| [Account Connections Pop Up Window](https://modmixx-427f89e87a1b.herokuapp.com/social/connections/) _login required_ | `/social/connections/` | ✅ | ![Account Connections validation screenshot](docs/images/test-screenshots/account-connections-html-validation.png) | Login required - validated by copying page source into the W3C validator’s “Validate by Direct Input” option. | Popup window |
| [Third Party Connect Pop Up Window](https://modmixx-427f89e87a1b.herokuapp.com/google/login/?process=connect) _login required_ | `/google/login/?process=connect` | ✅ | ![Connect google validation screenshot](docs/images/test-screenshots/connect-google-html-validation.png) | Login required - validated by copying page source into the W3C validator’s “Validate by Direct Input” option. | Popup window |
| [Delete Account Warning Page](https://modmixx-427f89e87a1b.herokuapp.com/accounts/delete/) _login required_ | `/delete/` | ✅ | ![delete account validation screenshot](docs/images/test-screenshots/delete-account-html-validation.png) | Login required - validated by copying page source into the W3C validator’s “Validate by Direct Input” option. | Confirm delete |
| [Logged In/Feed/Discover Page](https://modmixx-427f89e87a1b.herokuapp.com/tracks/) _login required_ | `/tracks/` | ✅ | ![Feed validation screenshot](docs/images/test-screenshots/feed-html-validation.png) | Login required - validated by copying page source into the W3C validator’s “Validate by Direct Input” option. | Fixed: removed controlslist attribute for mvp (future plans to build custom audio player) |
| Edit Track Page - _login and track owner required_| `/tracks/owners-track-name/edit/` | ✅ | ![Edit Track validation screenshot](docs/images/test-screenshots/edit-track-html-validation.png) | Track owner and login required - validated by copying page source into the W3C validator’s “Validate by Direct Input” option. | Fixed: Removed trailing slash from img tag and added missing help text for form accessibility. ![edit track errors screenshot](docs/images/test-screenshots/edit-track-html-errors.png) |
| [Track Detail Page](https://modmixx-427f89e87a1b.herokuapp.com/tracks/spectral/) _login required_ | `/tracks/spectral/` _example track slug_ | ✅ | ![Track Detail validation screenshot](docs/images/test-screenshots/track-detail-html-validation.png) | Login required - validated by copying page source into the W3C validator’s “Validate by Direct Input” option. | Fixed: removed controlslist attribute for mvp (future plans to build custom audio player) |
| [Error Page](https://modmixx-427f89e87a1b.herokuapp.com/nonexistent/) | `/nonexistent/` | ✅ | ![404 error screenshot](docs/images/test-screenshots/404-error-html-validation.png) |  | |
| 500 Error Page | `/test-500/` | ✅ | ![500 error screenshot](docs/images/test-screenshots/500-error-html-validation.png) | url not in production | Temporary test URL for 500 Server error - url not in production |

### Summary
- **Total Pages Tested:** 17
- **Pages Passed:** 17
- **Pages with Errors:** 0
- **Pages with Warnings:** 0

## CSS Validation

Testing with [W3C CSS Validator](https://jigsaw.w3.org/css-validator/).

All CSS files validated - no errors found.

![css validation screenshot](docs/images/test-screenshots/css-validation-results.png)

| File | Status | Notes |
|-----|--------|-------|
| base.css | ✅ |  |
| components.css | ✅ |  |
| layout.css | ✅ | The CSS mask property on the hero image with linear-gradient was flagging validation errors despite working correctly in all modern browsers. Alternative attempts included CSS gradient overlays with mix-blend-mode, pseudo-element approaches with various blend modes & SVG mask definitions. Fix: removed the CSS mask property entirely and achieved a similar soft fade effect by applying a gradient mask with Gaussian blur directly to the hero image in Photoshop. I considered leaving the error in place to avoid disrupting the existing design, but ultimately decided on a small visual compromise for ensured compatibility. |
| profile.css | ✅ |  |
| tracks.css | ✅ |  |
| variables.css | ✅ |  |

## JavaScript Validation

Testing with [JSHint](https://jshint.com/) and [ESLint](https://eslint.org/). Used both tools to ensure code quality and adherence to best practices.

| File | Status | JSHint Screenshot | ESLint Screenshot | Notes |
|-----|--------|-------|-------|-------|
| comments.js | ✅ | ![comments jshint](docs/images/test-screenshots/comments-jshint.png) | ![comments eslint](docs/images/test-screenshots/comments-eslint-terminal-no-errors.png) | Resolved all warnings & errors: ![eslint terminal warnings](docs/images/test-screenshots/comments-eslint-terminal-warnings.png) ![eslint terminal error](docs/images/test-screenshots/comments-eslint-terminal-warnings-quotes.png) |
| feed.js | ✅ | ![feed jshint](docs/images/test-screenshots/feed-jshint.png) | ![feed eslint](docs/images/test-screenshots/feed-eslint-terminal-no-errors.png) | Resolved all warnings & errors: ![eslint terminal warnings](docs/images/test-screenshots/feed-eslint-teminal-warnings-quotes.png) |
| popup-utils.js | ✅ | ![popup-utils jshint](docs/images/test-screenshots/popup-utils-jshint.png) | ![popup-utils-eslint](docs/images/test-screenshots/popup-utils-eslint.png) | No warnings or errors found. |
| profile-edit.js | ✅ | ![profile-edit jshint](docs/images/test-screenshots/profile-edit-jshint.png) | ![profile-edit eslint](docs/images/test-screenshots/profile-edit-eslint.png) | Resolved all warnings & errors: Fixed unused function warning with `/* exported connectGoogle */` ESLint directive - function is called from HTML "Connect Google" handler. ![eslint terminal warnings](docs/images/test-screenshots/profile-edit-eslint-warning.png) ![eslint terminal error](docs/images/test-screenshots/profile-edit-eslint-error.png) | 
| profile.js | ✅ | ![profile jshint](docs/images/test-screenshots/profile-jshint.png) | ![profile eslint](docs/images/test-screenshots/profile-eslint.png) | No warnings or errors found. |
| upload.js | ✅ | ![upload jshint](docs/images/test-screenshots/upload-jshint.png) | ![upload eslint](docs/images/test-screenshots/upload-eslint.png) | Resolved all warnings & errors: Added `/* global bootstrap, DataTransfer */` for jshint to recognize these globals provided by browser/bootstrap. |
| utilities.js | ✅ | ![utilities jshint](docs/images/test-screenshots/utilities-jshint.png) | ![utilities eslint](docs/images/test-screenshots/utilities-eslint.png) | No warnings or errors found. |

## Python Code Quality

All Python files validated using multiple tools to ensure comprehensive code quality and PEP8 compliance.

### Validation Tools
- **[Flake8](https://flake8.pycqa.org/)**: PEP8 compliance and error detection
- **[Black](https://black.readthedocs.io/)**: Code formatting with 79-character line length  
- **[isort](https://pycqa.github.io/isort/)**: Import organization following Django conventions
- **[Code Institute PEP8 Linter](https://pep8ci.herokuapp.com/)**: Final validation check

### Configuration
- **Line length**: 79 characters
- **Import organization**: Django imports → third-party → local imports
- **Configuration files**: `.flake8`, `pyproject.toml`

| App | Files Checked | Flake8 Status | Screenshot | Notes |
|-----|---------------|---------------|------------|-------|
| accounts | 8 files | ✅ | ![accounts flake8](docs/images/test-screenshots/all-accounts-files-flake8.png) | Fixed E501 (line length), F401 (unused imports) |
| comments | 7 files | ✅ | ![comments flake8](docs/images/test-screenshots/all-comments-app-flake8.png) | Resolved F401 issues, applied formatting |
| contact | 7 files | ✅ | ![contact flake8](docs/images/test-screenshots/all-contact-app-flake8.png) | Removed unused imports, fixed line lengths |
| core | 7 files | ✅ | ![core flake8](docs/images/test-screenshots/all-core-app-flake8.png) | No models - utility app structure |
| tracks | 8 files | ✅ | ![tracks flake8](docs/images/test-screenshots/all-tracks-app-flake8.png) | Fixed E501, F401, F841 issues |
| modmixx | 4 files | ✅ | ![modmixx flake8](docs/images/test-screenshots/all-modmixx-app-flake8.png) | Settings file line length fixes |

### Summary
- **Total Python files**: 41
- **Apps with violations**: 0
- **PEP8 compliant**: ✅ All files pass
- **Last validated**: [23/08/2025]

### Key Improvements Applied
- Fixed line length violations (E501) across all apps
- Removed unused imports (F401) from views, models, and forms
- Organized imports with isort following Django conventions:
  - Django imports grouped first
  - Third-party imports second  
  - Local application imports last
  - Alphabetical ordering within groups
- Eliminated unused variables (F841) in exception handling
- Applied consistent code formatting via Black
- Enhanced docstrings throughout all applications


## Lighthouse Performance Testing

All pages tested using [Google Lighthouse](https://developers.google.com/web/tools/lighthouse) for performance, accessibility, best practices, and SEO optimization. Testing conducted on both desktop and mobile devices to ensure responsive performance.

### Performance Results

| Page | Desktop Results | Mobile Results | Notes |
|------|----------------|----------------|-------|
| Home | ![Home Desktop](docs/images/test-screenshots/lighthouse/home-lighthouse-desktop.png) | ![Home Mobile](docs/images/test-screenshots/lighthouse/home-lighthouse-mobile.png) |  |
| About | ![About Desktop](docs/images/test-screenshots/lighthouse/about-lighthouse-desktop.png) | ![About Mobile](docs/images/test-screenshots/lighthouse/about-lighthouse-mobile.png) |  |
| Contact | ![Contact Desktop](docs/images/test-screenshots/lighthouse/contact-lighthouse-desktop.png) | ![Contact Mobile](docs/images/test-screenshots/lighthouse/contact-lighthouse-mobile.png) |  |
| Sign Up | ![Signup Desktop](docs/images/test-screenshots/lighthouse/signup-lighthouse-desktop.png) | ![Signup Mobile](docs/images/test-screenshots/lighthouse/signup-lighthouse-mobile.png) |  |
| Login | ![Login Desktop](docs/images/test-screenshots/lighthouse/login-lighthouse-desktop.png) | ![Login Mobile](docs/images/test-screenshots/lighthouse/login-lighthouse-mobile.png) | Google button contrast improved |
| Track Feed | ![Feed Desktop](docs/images/test-screenshots/lighthouse/feed-lighthouse-desktop.png) | ![Feed Mobile](docs/images/test-screenshots/lighthouse/feed-lighthouse-mobile.png) |  |
| Track Detail | ![Track Desktop](docs/images/test-screenshots/lighthouse/track-detail-lighthouse-desktop.png) | ![Track Mobile](docs/images/test-screenshots/lighthouse/track-detail-lighthouse-mobile.png) |  |
| Profile View | ![Profile Desktop](docs/images/test-screenshots/lighthouse/profile-lighthouse-desktop.png) | ![Profile Mobile](docs/images/test-screenshots/lighthouse/profile-lighthouse-mobile.png) |  |
| Profile Edit | ![Edit Desktop](docs/images/test-screenshots/lighthouse/profile-edit-lighthouse-desktop.png) | ![Edit Mobile](docs/images/test-screenshots/lighthouse/profile-edit-lighthouse-mobile.png) |  |
| Delete Account | ![Delete Desktop](docs/images/test-screenshots/lighthouse/delete-account-lighthouse-desktop.png) | ![Delete Mobile](docs/images/test-screenshots/lighthouse/delete-account-lighthouse-mobile.png) |  |
| Edit Track | ![Edit Track Desktop](docs/images/test-screenshots/lighthouse/edit-track-lighthouse-desktop.png) | ![Edit Track Mobile](docs/images/test-screenshots/lighthouse/edit-track-lighthouse-mobile.png) |  |
| Third Party Connections | ![Third Party Desktop](docs/images/test-screenshots/lighthouse/thirdparty-lighthouse-desktop.png) | ![Third Party Mobile](docs/images/test-screenshots/lighthouse/thirdparty-lighthouse-mobile.png) |  |


