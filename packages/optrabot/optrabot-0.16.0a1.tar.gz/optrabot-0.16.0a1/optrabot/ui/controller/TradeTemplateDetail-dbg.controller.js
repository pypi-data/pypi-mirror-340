"use strict";

sap.ui.define(["./BaseController"], function (__BaseController) {
  "use strict";

  function _interopRequireDefault(obj) {
    return obj && obj.__esModule && typeof obj.default !== "undefined" ? obj.default : obj;
  }
  const BaseController = _interopRequireDefault(__BaseController);
  /**
   * @namespace com.optrabot.ui.controller
   */
  const TradeTemplateDetail = BaseController.extend("com.optrabot.ui.controller.TradeTemplateDetail", {
    onInit: function _onInit() {
      var oOwnerComponent = this.getOwnerComponent();
      this.oRouter = oOwnerComponent.getRouter();
      this.oControlModel = oOwnerComponent.getModel("control");
      this.oRouter.getRoute("template").attachPatternMatched(this._onTemplateMatched, this);
      this.oRouter.getRoute("templateWOLayout").attachPatternMatched(this._onTemplateMatched, this);
    },
    onEditToggleButtonPress: function _onEditToggleButtonPress() {
      var oTemplatePage = this.getView().byId("TemplatePageLayout");
      var bCurrentShowFooterState = oTemplatePage.getShowFooter();
      oTemplatePage.setShowFooter(!bCurrentShowFooterState);
    },
    _onTemplateMatched: function _onTemplateMatched(oEvent) {
      console.log("Template matched");
      this._template = oEvent.getParameter("arguments").template || this._template || "0";

      // Store the current template in the model
      var layout = oEvent.getParameter("arguments").layout || "TwoColumnsMidExpanded";
      this.oControlModel.setProperty("/currentLayout", layout);
      this.getView().bindElement({
        path: "/TemplateCollection/" + this._template,
        model: "tradetemplates"
      });
    },
    onFullscreenPressed: function _onFullscreenPressed() {
      var sCurrentLayout = this.oControlModel.getProperty("/currentLayout");
      var sNewLayout = sCurrentLayout;
      if (sCurrentLayout === "MidColumnFullScreen") {
        sNewLayout = "TwoColumnsMidExpanded";
      } else if (sCurrentLayout === "TwoColumnsMidExpanded") {
        sNewLayout = "MidColumnFullScreen";
      }
      this.oRouter.navTo("template", {
        layout: sNewLayout,
        template: this._template
      }, true);
    },
    onClosePressed: function _onClosePressed() {
      this.oRouter.navTo("templates", {
        layout: "OneColumn"
      }, true);
    },
    onExit: function _onExit() {
      this.oRouter.getRoute("template").detachPatternMatched(this._onTemplateMatched, this);
      this.oRouter.getRoute("templateWOLayout").detachPatternMatched(this._onTemplateMatched, this);
    }
  });
  return TradeTemplateDetail;
});
//# sourceMappingURL=TradeTemplateDetail-dbg.controller.js.map
