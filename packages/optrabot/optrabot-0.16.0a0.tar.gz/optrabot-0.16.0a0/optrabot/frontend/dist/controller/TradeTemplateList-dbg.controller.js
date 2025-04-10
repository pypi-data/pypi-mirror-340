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
  const TradeTemplateList = BaseController.extend("com.optrabot.ui.controller.TradeTemplateList", {
    onInit: function _onInit() {
      this.oView = this.getView();
      this.oRouter = this.getOwnerComponent().getRouter();
    },
    onTemplatePress: function _onTemplatePress(oEvent) {
      var oFCL = this.oView.getParent().getParent();
      oFCL.setLayout("TwoColumnsMidExpanded");
      var templatePath = oEvent.getSource().getBindingContext("tradetemplates").getPath();
      var templateName = templatePath.split("/").slice(-1).pop();
      console.log("Template name: " + templateName);
      this.oRouter.navTo("template", {
        layout: "TwoColumnsMidExpanded",
        template: templateName
      });
    }
  });
  return TradeTemplateList;
});
//# sourceMappingURL=TradeTemplateList-dbg.controller.js.map
