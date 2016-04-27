/// <reference path="typings/jquery.d.ts" />
var ConsolePage = (function () {
    /**
     * Describes the page
     * @param pageId ID of the page (internal)
     * @param name Name to print
     */
    function ConsolePage(pageId, name) {
        this.pageId = pageId;
        this.name = name;
        this.navId = "nav-" + name.toLowerCase();
    }
    /**
     * Returns an LI element to be added in the dynamic-navbar UL
     */
    ConsolePage.prototype.makeNavEntry = function () {
        // This will be added in a <ul> block
        return "<li id=\"" + this.navId + "\"><a href=\"javascript:show('" + this.pageId + "')\">" + this.name + "</a></li>\n";
    };
    /**
     * Shows the content received from the server
     * @param contentElement The content DIV
     * @param data HTML data received from the server
     */
    ConsolePage.prototype.showContent = function (contentElement, rel_url, data) {
        history.pushState({}, "Pelix Web Console", rel_url);
        updateNavBarState(this);
        contentElement.innerHTML = data;
        $(function () {
            $("table")['tablesorter']();
        });
    };
    /**
     * Show an error in the content element
     * @param contentElement The content DIV
     */
    ConsolePage.prototype.showError = function (contentElement) {
        contentElement.innerHTML = "<h1>Error</h1>\n<p>Something went wrong when grabbing information for page <i>" + this.name + "</i></p>";
    };
    /**
     * Get the page content using a REST request
     * @param contentElement The content DIV
     */
    ConsolePage.prototype.show = function () {
        this.showSubPage('content');
    };
    /**
     * Show a sub page
     * @param subUrl Sub-URL
     */
    ConsolePage.prototype.showSubPage = function (subUrl) {
        var _this = this;
        var contentElement = document.getElementById("content");
        var rel_url = "#" + this.pageId + "/" + subUrl;
        $.ajax("api/v1/page/" + this.pageId + "/" + subUrl, {
            dataType: 'html',
            success: function (data) { return _this.showContent(contentElement, rel_url, data); },
            error: function () { return _this.showError(contentElement); },
        });
    };
    return ConsolePage;
}());
// Define global accesses to pages
var GlobalConsolePages = new Array();
// Simplify the access to a console page bean
var GlobalPagesIDs = {};
// Global access to the current page
var GlobalCurrentPage = null;
/**
 * Shows the loading page
 */
function showLoading() {
    var content = document.getElementById("content");
    content.innerHTML = '<h2><img src="imgs/loading.gif" alt="Loading..." /> Loading...</h2>';
}
/**
 * Set the given page as the active one in the navigation bar
 * @param page The active page
 */
function updateNavBarState(page) {
    // Change the active page in the navigation bar
    var navbar_root = document.getElementById("dynamic-navbar-root");
    var active_element = navbar_root.getElementsByClassName("active")[0];
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
function show(page_id) {
    // Get the ConsolePage object
    var page = GlobalPagesIDs[page_id];
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
function updateNavBar(data) {
    // Convert data to ConsolePage objects
    var data_pages = data["pages"];
    var data_names = data["names"];
    for (var idx in data_pages) {
        GlobalConsolePages.push(new ConsolePage(data_pages[idx], data_names[idx]));
    }
    // Update the ID -> ContentPage dictionary
    GlobalConsolePages.forEach(function (page) {
        GlobalPagesIDs[page.pageId] = page;
    });
    // Set the content of the navigation bar
    var navbar = document.getElementById("dynamic-navbar");
    GlobalConsolePages.forEach(function (page) {
        navbar.innerHTML += page.makeNavEntry();
    });
    // Get the current page, if available
    // Use substring to remove the starting '#'
    var activeLocation = window.location.hash.substring(1);
    var activePageId = activeLocation;
    var subUrl = "";
    var pageIdSepIdx = activeLocation.indexOf("/");
    if (pageIdSepIdx > 0) {
        activePageId = activeLocation.substring(0, pageIdSepIdx);
        subUrl = activeLocation.substring(pageIdSepIdx + 1);
    }
    if (!subUrl) {
        subUrl = "content";
    }
    var activePage = GlobalPagesIDs[activePageId];
    if (activePage != undefined) {
        // The Page exists
        GlobalCurrentPage = activePage;
        activePage.showSubPage(subUrl);
        updateNavBarState(activePage);
    }
    else {
        // Show the main page
        show(data["main"]);
    }
}
/**
 * Prepare the page content
 */
window.onload = function () {
    // Show the loading page
    showLoading();
    // Request the list of pages
    function getPages() {
        $.ajax("api/v1/pages", {
            dataType: 'json',
            success: updateNavBar,
            error: function () {
                // Recall the method after 5s
                console.error("Error retrieving the list pages");
                setTimeout(function () { return getPages(); }, 5000);
            }
        });
    }
    ;
    getPages();
};
//# sourceMappingURL=app.js.map
