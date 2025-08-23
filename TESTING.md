# Testing Documentation

### Contents
1. [HTML Validation](#html-validation)
2. [CSS Validation](#css-validation)
3. [JavaScript Linting](#javascript-linting)

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


| File | Status | JSHint Screenshot | ESLint Screenshot | Notes |
|-----|--------|-------|-------|-------|
| comments.js | ✅ | ![comments jshint](docs/images/test-screenshots/comments-jshint.png) | ![comments eslint](docs/images/test-screenshots/comments-eslint-terminal-no-errors.png) | Resolved all warnings: ![eslint terminal warnings](docs/images/test-screenshots/comments-eslint-terminal-warnings.png) ![eslint terminal error](docs/images/test-screenshots/comments-eslint-terminal-warnings-quotes.png) |