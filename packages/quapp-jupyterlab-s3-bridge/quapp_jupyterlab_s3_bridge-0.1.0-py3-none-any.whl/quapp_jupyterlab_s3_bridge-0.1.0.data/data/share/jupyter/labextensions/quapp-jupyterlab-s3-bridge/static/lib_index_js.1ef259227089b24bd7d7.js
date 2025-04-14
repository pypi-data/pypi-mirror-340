"use strict";
(self["webpackChunkquapp_jupyterlab_s3_bridge"] = self["webpackChunkquapp_jupyterlab_s3_bridge"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_5__);






/**
 * Widget chứa dropdown list hiển thị version.
 * Khi tải, gọi GET /s3bridge/versions để lấy danh sách phiên bản.
 * Và khi có sự thay đổi, gọi PATCH /s3bridge/versions/<selected_version> để cập nhật file list.
 */
class VersionsDropdownWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget {
    constructor() {
        super();
        this.addClass('versions-dropdown-widget');
        this._select = document.createElement('select');
        this._select.style.margin = '0 4px';
        this._select.style.width = '150px';
        this.node.appendChild(this._select);
        this.loadVersions();
        // Sự kiện khi lựa chọn phiên bản thay đổi
        this._select.addEventListener("change", async () => {
            const selectedVersion = this.selectedVersion;
            console.log(`Version changed: ${selectedVersion}`);
            try {
                const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_5__.ServerConnection.makeSettings();
                // Gọi PATCH đến /s3bridge/versions/<selectedVersion>
                const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__.URLExt.join(settings.baseUrl, 's3bridge', 'versions', selectedVersion);
                const response = await fetch(url, { method: 'PATCH', credentials: 'include' });
                if (!response.ok) {
                    const errData = await response.json();
                    throw new Error(`Update error: ${response.status} => ${errData.error || ''}`);
                }
                const result = await response.json();
                console.log("Version update successful:", result);
                // Sau khi cập nhật file list thành công, refresh lại dropdown
                await this.loadVersions();
            }
            catch (error) {
                console.error("Error updating version:", error);
            }
        });
    }
    async loadVersions() {
        try {
            const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_5__.ServerConnection.makeSettings();
            const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__.URLExt.join(settings.baseUrl, 's3bridge', 'versions');
            const response = await fetch(url, { method: 'GET', credentials: 'include' });
            if (!response.ok) {
                throw new Error(`Failed to load versions: ${response.status}`);
            }
            const result = await response.json();
            const versionsData = result.data;
            const versionNumbers = versionsData.map(item => Number(item.version));
            versionNumbers.sort((a, b) => a - b);
            this._select.innerHTML = "";
            versionNumbers.forEach(v => {
                const option = document.createElement('option');
                option.value = v.toString();
                option.textContent = `v${v}`;
                this._select.appendChild(option);
            });
            if (versionNumbers.length > 0) {
                // Chọn phiên bản mới nhất làm mặc định
                this._select.value = versionNumbers[versionNumbers.length - 1].toString();
            }
            console.log("Loaded versions from server:", versionNumbers);
        }
        catch (error) {
            console.error("Error loading versions:", error);
        }
    }
    get selectedVersion() {
        return this._select.value;
    }
}
/**
 * Tạo toolbar chứa label "Version:" và dropdown list.
 */
function createVersionToolbar() {
    const versionToolbar = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget();
    versionToolbar.addClass('jp-FileBrowser-version-toolbar');
    versionToolbar.node.style.display = 'flex';
    versionToolbar.node.style.alignItems = 'center';
    versionToolbar.node.style.padding = '2px 4px';
    versionToolbar.node.style.borderTop = '1px solid var(--jp-border-color2)';
    const label = document.createElement('span');
    label.textContent = 'Version:';
    label.style.marginLeft = '8px';
    label.style.marginRight = '4px';
    const dropdown = new VersionsDropdownWidget();
    versionToolbar.node.appendChild(label);
    versionToolbar.node.appendChild(dropdown.node);
    return versionToolbar;
}
/**
 * Hàm chèn nút "Save to S3" vào toolbar của FileBrowser.
 * Sau khi upload thành công, phát event refresh để làm mới dropdown.
 */
function addSaveButton(browser) {
    console.log('Adding Save to S3 button to FileBrowser:', browser.id);
    const saveButton = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.ToolbarButton({
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.saveIcon,
        tooltip: 'Push local changes to S3 backend',
        onClick: async () => {
            console.log('Save to S3 button clicked');
            try {
                const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_5__.ServerConnection.makeSettings();
                const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__.URLExt.join(settings.baseUrl, 's3bridge', 'upload-s3');
                const resp = await fetch(url, { method: 'POST', credentials: 'include' });
                if (!resp.ok) {
                    const errData = await resp.json();
                    throw new Error(`Upload error: ${resp.status} => ${errData.error || ''}`);
                }
                const data = await resp.json();
                alert('Upload success: ' + JSON.stringify(data));
                // Phát sự kiện để refresh dropdown phiên bản
                document.dispatchEvent(new CustomEvent("refreshVersionDropdown"));
            }
            catch (err) {
                console.error(err);
                alert('Upload failed: ' + err);
            }
        }
    });
    saveButton.node.id = 'saveS3Button';
    setTimeout(() => {
        if (browser.toolbar) {
            if (!browser.toolbar.node.querySelector('#saveS3Button')) {
                try {
                    browser.toolbar.insertItem(1, 'saveS3', saveButton);
                    console.log('Save to S3 button inserted at index 1 in', browser.id);
                }
                catch (error) {
                    console.warn('insertItem failed, trying addItem instead:', error);
                    browser.toolbar.addItem('saveS3', saveButton);
                }
            }
            else {
                console.log('Save to S3 button already exists in', browser.id);
            }
        }
        else {
            console.warn('Toolbar not ready for', browser.id);
        }
    }, 200);
}
/**
 * Hàm chèn hàng toolbar chứa dropdown version vào layout của FileBrowser.
 * Lắng nghe sự kiện "refreshVersionDropdown" để làm mới dropdown.
 */
function addVersionToolbar(browser) {
    console.log('Adding version dropdown toolbar to FileBrowser:', browser.id);
    const layout = browser.layout;
    if (!layout) {
        console.warn('No layout available for', browser.id);
        return;
    }
    const existing = browser.node.querySelector('.jp-FileBrowser-version-toolbar');
    if (existing) {
        console.log('Version toolbar already exists for', browser.id);
        return;
    }
    const versionToolbar = createVersionToolbar();
    // Lắng nghe event refresh để reload dropdown
    document.addEventListener("refreshVersionDropdown", async () => {
        console.log("Refreshing version dropdown for", browser.id);
        // Giả sử bạn có thể lấy lại tham chiếu widget dropdown thông qua DOM,
        // ở đây chúng ta reload toàn bộ toolbar bằng cách loại bỏ và chèn lại.
        versionToolbar.node.innerHTML = "";
        const label = document.createElement('span');
        label.textContent = 'Version:';
        label.style.marginLeft = '8px';
        label.style.marginRight = '4px';
        versionToolbar.node.appendChild(label);
        const newDropdown = new VersionsDropdownWidget();
        versionToolbar.node.appendChild(newDropdown.node);
    });
    layout.insertWidget(1, versionToolbar);
    console.log('Version dropdown toolbar inserted in', browser.id);
}
/**
 * Plugin extension: thêm nút "Save to S3" và toolbar chứa dropdown version vào FileBrowser.
 */
const plugin = {
    id: 'quapp_jupyterlab_s3_bridge:plugin',
    description: 'A JupyterLab extension for project Quapp: Save local changes to S3.',
    autoStart: true,
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_0__.IFileBrowserFactory],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__.ISettingRegistry],
    activate: (app, factory, settingRegistry) => {
        console.log('Activating quapp_jupyterlab_s3_bridge extension with dynamic version dropdown');
        if (settingRegistry) {
            settingRegistry
                .load(plugin.id)
                .then(settings => {
                console.log('Settings loaded:', settings.composite);
            })
                .catch(reason => {
                console.error('Failed to load settings for quapp_jupyterlab_s3_bridge.', reason);
            });
        }
        function addToolbarItems(browser) {
            addSaveButton(browser);
            addVersionToolbar(browser);
        }
        factory.tracker.forEach((browser) => {
            addToolbarItems(browser);
        });
        factory.tracker.widgetAdded.connect((sender, browser) => {
            console.log('New FileBrowser widget added:', browser.id);
            addToolbarItems(browser);
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.1ef259227089b24bd7d7.js.map