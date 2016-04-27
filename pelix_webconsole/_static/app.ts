/// <reference path="typings/jquery.d.ts" />

class ConsolePage {
    // Element ID in the navigation bar
    navId: string;

    /**
     * Describes the page
     * @param pageId ID of the page (internal)
     * @param name Name to print
     */
    constructor(public pageId: string, public name: string) {
        this.navId = "nav-" + name.toLowerCase();
    }

    /**
     * Returns an LI element to be added in the dynamic-navbar UL
     */
    makeNavEntry() {
        // This will be added in a <ul> block
        return `<li id="${this.navId}"><a href="javascript:show('${this.pageId}')">${this.name}</a></li>\n`
    }

    /**
     * Shows the content received from the server
     * @param contentElement The content DIV
     * @param data HTML data received from the server
     */
    showContent(contentElement: HTMLDivElement, rel_url: string, data) {
        history.pushState({}, "Pelix Web Console", rel_url);
        updateNavBarState(this);
        contentElement.innerHTML = data;

        $(function () {
            $("table")['tablesorter']();
        });
    }

    /**
     * Show an error in the content element
     * @param contentElement The content DIV
     */
    showError(contentElement: HTMLDivElement) {
        contentElement.innerHTML = `<h1>Error</h1>\n<p>Something went wrong when grabbing information for page <i>${this.name}</i></p>`;
    }

    /**
     * Get the page content using a REST request
     * @param contentElement The content DIV
     */
    show() {
        this.showSubPage('content');
    }

    /**
     * Show a sub page
     * @param subUrl Sub-URL
     */
    showSubPage(subUrl: string) {
        let contentElement = <HTMLDivElement>document.getElementById("content");
        let rel_url = `#${this.pageId}/${subUrl}`;

        $.ajax(`api/v1/page/${this.pageId}/${subUrl}`, {
            dataType: 'html',
            success: (data) => this.showContent(contentElement, rel_url, data),
            error: () => this.showError(contentElement),
        });
    }
}

// Define global accesses to pages
const GlobalConsolePages = new Array<ConsolePage>();
// Simplify the access to a console page bean
const GlobalPagesIDs: { [id: string]: ConsolePage } = {};

// Global access to the current page
var GlobalCurrentPage = null;

/**
 * Shows the loading page
 */
function showLoading() {
    let content = document.getElementById("content");
    content.innerHTML = '<h2><img src="imgs/loading.gif" alt="Loading..." /> Loading...</h2>';
}

/**
 * Set the given page as the active one in the navigation bar
 * @param page The active page
 */
function updateNavBarState(page: ConsolePage) {
    // Change the active page in the navigation bar
    let navbar_root = document.getElementById("dynamic-navbar-root");
    let active_element = navbar_root.getElementsByClassName("active")[0];
    if (active_element != undefined) {
        active_element.setAttribute("class", "");
    }

    // Get the Page ID in the navigation bar and activate it
    document.getElementById(page.navId).setAttribute("class", "active");
}

/**
 * Show the page matching the given page ID
 * @param page_id Page ID
 */
function show(page_id: string) {
    // Get the ConsolePage object
    let page = GlobalPagesIDs[page_id];
    if (page == undefined) {
        // Page not found
        return;
    }

    // Change the active page in the navigation bar
    updateNavBarState(page);

    // Show the loading page
    showLoading();

    // Set the page content
    GlobalCurrentPage = page;
    page.show();
}

/**
 * Updates the content of the navigation bar
 * @param data List of modules given by the server
 */
function updateNavBar(data: Object) {
    // Convert data to ConsolePage objects
    let data_pages = data["pages"]
    let data_names = data["names"]
    for (var idx in data_pages) {
        GlobalConsolePages.push(new ConsolePage(data_pages[idx], data_names[idx]));
    }

    // Update the ID -> ContentPage dictionary
    GlobalConsolePages.forEach((page) => {
        GlobalPagesIDs[page.pageId] = page;
    });

    // Set the content of the navigation bar
    let navbar = document.getElementById("dynamic-navbar");
    GlobalConsolePages.forEach((page) => {
        navbar.innerHTML += page.makeNavEntry();
    });

    // Get the current page, if available
    // Use substring to remove the starting '#'
    let activeLocation = window.location.hash.substring(1);
    let activePageId = activeLocation;
    let subUrl = "";

    let pageIdSepIdx = activeLocation.indexOf("/");
    if (pageIdSepIdx > 0) {
        activePageId = activeLocation.substring(0, pageIdSepIdx);
        subUrl = activeLocation.substring(pageIdSepIdx + 1);
    }

    if (!subUrl) {
        subUrl = "content";
    }

    let activePage = GlobalPagesIDs[activePageId];
    if (activePage != undefined) {
        // The Page exists
        GlobalCurrentPage = activePage;
        activePage.showSubPage(subUrl);
        updateNavBarState(activePage);
    } else {
        // Show the main page
        show(data["main"]);
    }
}

/**
 * Prepare the page content
 */
window.onload = () => {
    // Show the loading page
    showLoading();

    // Request the list of pages
    function getPages() {
        $.ajax("api/v1/pages", {
            dataType: 'json',
            success: updateNavBar,
            error: () => {
                // Recall the method after 5s
                console.error("Error retrieving the list pages");
                setTimeout(() => getPages(), 5000);
            }
        });
    };
    getPages();
};
