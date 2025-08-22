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
| [Login Page](https://modmixx-427f89e87a1b.herokuapp.com/accounts/login/) | `/login/` |  |  | [Login Result](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Fmodmixx-427f89e87a1b.herokuapp.com%2Faccounts%2Flogin%2F) |  |
| [Third Party Login Page](https://modmixx-427f89e87a1b.herokuapp.com/accounts/social/login/) | `/social/login/` |  |  | [Third Party Login Result](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Fmodmixx-427f89e87a1b.herokuapp.com%2Faccounts%2Fsocial%2Flogin%2F) | Google login |
| [Profile Set Up Page](https://modmixx-427f89e87a1b.herokuapp.com/accounts/profile/setup/) | `/profile/setup/` |  |  | [Profile Set Up Result](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Fmodmixx-427f89e87a1b.herokuapp.com%2Faccounts%2Fprofile%2Fsetup%2F) | After signup |
| [Profile Page](https://modmixx-427f89e87a1b.herokuapp.com/profile/jools/) | `/profile/jools/` |  |  | [Profile Result](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Fmodmixx-427f89e87a1b.herokuapp.com%2Fprofile%2Fjools%2F) | Example profile username url |
| [Profile Edit Page](https://modmixx-427f89e87a1b.herokuapp.com/profile/jools/edit/) | `/profile/jools/edit/` |  |  | [Profile Edit Result](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Fmodmixx-427f89e87a1b.herokuapp.com%2Fprofile%2Fjools%2Fedit%2F) | Example profile edit username url |
| [Account Connections Pop Up Window](https://modmixx-427f89e87a1b.herokuapp.com/accounts/social/connections/) | `/social/connections/` |  |  | [Account Connections Result](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Fmodmixx-427f89e87a1b.herokuapp.com%2Faccounts%2Fsocial%2Fconnections%2F) | Popup window |
| [Third Party Connect Pop Up Window](https://modmixx-427f89e87a1b.herokuapp.com/google/login/?process=connect) | `/google/login/?process=connect` |  |  | [Third Party Connect Result](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Fmodmixx-427f89e87a1b.herokuapp.com%2Fgoogle%2Flogin%2F%3Fprocess%3Dconnect) | Popup window |
| [Delete Account Warning Page](https://modmixx-427f89e87a1b.herokuapp.com/accounts/delete/) | `/delete/` |  |  | [Delete Account Warning Result](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Fmodmixx-427f89e87a1b.herokuapp.com%2Faccounts%2Fdelete%2F) | Confirm delete |
| [Logged In/Feed/Discover Page](https://modmixx-427f89e87a1b.herokuapp.com/tracks/) | `/tracks/` |  |  | [Logged In/Feed/Discover Result](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Fmodmixx-427f89e87a1b.herokuapp.com%2Ftracks%2F) | Fixed: removed controlslist attribute for mvp (future plans to build custom audio player) |
| [Upload Track](https://modmixx-427f89e87a1b.herokuapp.com/tracks/?share=1) | `/tracks/?share=1` |  |  | [Upload Track Result](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Fmodmixx-427f89e87a1b.herokuapp.com%2Ftracks%2F%3Fshare%3D1) | Upload modal |
| [Track Detail Page](https://modmixx-427f89e87a1b.herokuapp.com/tracks/spectral/) | `/tracks/spectral/` |  |  | [Track Detail Result](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Fmodmixx-427f89e87a1b.herokuapp.com%2Ftracks%2Fspectral%2F) | Example track slug url |
| [Error Page](https://modmixx-427f89e87a1b.herokuapp.com/nonexistent/) | `/nonexistent/` |  |  | [Error Page Result](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Fmodmixx-427f89e87a1b.herokuapp.com%2Fnonexistent%2F) | 404 error |
| [500 Page](https://modmixx-427f89e87a1b.herokuapp.com/test-500/) | `/test-500/` |  |  | [500 Page Result](https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F%2Fmodmixx-427f89e87a1b.herokuapp.com%2Ftest-500%2F) | Temporary test URL for 500 error - url not in production |

### Summary
- **Total Pages Tested:** 0
- **Pages Passed:** 
- **Pages with Errors:** 0
- **Pages with Warnings:** 0

## CSS Validation

Testing with [W3C CSS Validator](https://jigsaw.w3.org/css-validator/).
