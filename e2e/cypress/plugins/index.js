/// <reference types="cypress" />
// ***********************************************************
// This example plugins/index.js can be used to load plugins
//
// You can change the location of this file or turn off loading
// the plugins file with the 'pluginsFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/plugins-guide
// ***********************************************************

// This function is called when a project is opened or re-opened (e.g. due to
// the project's config changing)

/**
 * @type {Cypress.PluginConfig}
 */
const cucumber = require("cypress-cucumber-preprocessor").default;
const browserify = require("@cypress/browserify-preprocessor");


module.exports = (on, config) => {
	// `on` is used to hook into various events Cypress emits
	// `config` is the resolved Cypress config
	const options = browserify.defaultOptions;
	options.browserifyOptions.plugin.unshift([
		"tsify",
		{ project: "../../tsconfig.json" },
	]);
	on("file:preprocessor", cucumber(options));

	on("before:browser:launch", (browser = {}, launchOptions) => {
		// `args` is an array of all the arguments that will
		// be passed to browsers when it launches

		// if (browser.family === 'chromium' && browser.name !== 'electron') {
		// see: https://github.com/cypress-io/cypress/issues/3633
		launchOptions.args.push("--disable-dev-shm-usage");
		// launchOptions.args.push('--disable-popup-blocking');
		// launchOptions.args.push('--safebrowsing-disable-download-protection');
		// launchOptions.args.push('--safebrowsing-disable-extension-blacklist');
		// launchOptions.preferences["download.prompt_for_download"] = false
		// launchOptions.preferences["safebrowsing.enabled"] = true
		// launchOptions.preferences["download.default_directory"] = "cypress/downloads"

		// whatever you return here becomes the launchOptions
		return launchOptions;
		// }
	});

};
