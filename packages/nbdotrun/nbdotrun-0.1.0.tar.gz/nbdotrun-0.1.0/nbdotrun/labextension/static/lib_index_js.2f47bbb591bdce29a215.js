"use strict";
(self["webpackChunknbdotrun"] = self["webpackChunknbdotrun"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__);



const PLUGIN_NAME = 'nbdotrun';
const PLUGIN_ID = `${PLUGIN_NAME}:plugin`;
function throttle(fn, delay) {
    let timeout = null;
    return () => {
        if (timeout) {
            return;
        }
        timeout = window.setTimeout(() => {
            fn();
            timeout = null;
        }, delay);
    };
}
function escapeRegExp(s) {
    return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
function shouldAutoExecute(text, triggerSymbol) {
    const lines = text.trimEnd().split('\n');
    const last = lines[lines.length - 1];
    const regex = new RegExp(`^\\s*${escapeRegExp(triggerSymbol)}\\s*$`);
    return regex.test(last);
}
function attachNotebookListener(panel, triggerSymbol) {
    // track which cells have been connected
    const connectedCells = new WeakSet();
    panel.context.ready.then(() => {
        const notebook = panel.content;
        const model = notebook.model;
        if (!model) {
            console.error(`${PLUGIN_NAME} Failed to retrieve notebook model`);
            return;
        }
        const throttledScan = throttle(() => {
            for (let i = 0; i < model.cells.length; i++) {
                const cellWidget = notebook.widgets[i];
                const cellModel = model.cells.get(i);
                if ((cellModel === null || cellModel === void 0 ? void 0 : cellModel.type) === 'code' && cellWidget instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__.CodeCell) {
                    const codeModel = cellModel;
                    const source = codeModel.sharedModel.getSource();
                    if (shouldAutoExecute(source, triggerSymbol)) {
                        console.log(`${PLUGIN_NAME} Executing cell ${i} due to terminal symbol match: "${triggerSymbol}"`);
                        // remove the trigger line
                        const newSource = source
                            .trimEnd()
                            .split('\n')
                            .slice(0, -1)
                            .join('\n');
                        codeModel.sharedModel.setSource(newSource);
                        void _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__.CodeCell.execute(cellWidget, panel.sessionContext);
                    }
                }
            }
        }, 300); // debounce time in ms
        // Initial hookup for existing cells
        for (let i = 0; i < model.cells.length; i++) {
            const cellModel = model.cells.get(i);
            if (!connectedCells.has(cellModel) && cellModel.type === 'code') {
                const codeModel = cellModel;
                codeModel.contentChanged.connect(throttledScan);
                connectedCells.add(codeModel);
            }
        }
        model.cells.changed.connect((_, changes) => {
            throttledScan();
            if (changes.type === 'add') {
                changes.newValues.forEach(cell => {
                    if (!connectedCells.has(cell) && cell.type === 'code') {
                        const codeModel = cell;
                        codeModel.contentChanged.connect(throttledScan);
                        connectedCells.add(codeModel);
                    }
                });
            }
        });
    });
}
function activateNbdotrun(app, notebooks, settings) {
    console.log(`JupyterLab extension ${PLUGIN_NAME} is activated!`);
    let triggerSymbol = '.';
    if (settings) {
        settings
            .load(PLUGIN_ID)
            .then(settings => {
            triggerSymbol = settings.get('triggerSymbol').composite;
        })
            .catch(reason => {
            console.error(`${PLUGIN_NAME} Failed to load settings`, reason);
        });
    }
    notebooks.widgetAdded.connect((_, panel) => {
        attachNotebookListener(panel, triggerSymbol);
    });
    notebooks.forEach(panel => attachNotebookListener(panel, triggerSymbol));
}
/**
 * Initialization data for the nbdotrun extension.
 */
const plugin = {
    id: PLUGIN_ID,
    description: 'A JupyterLab extension that will listen for code cell changes and run if ending in dot (`.`).',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__.ISettingRegistry],
    activate: activateNbdotrun
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.2f47bbb591bdce29a215.js.map