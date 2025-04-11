import Router from "sap/ui/core/routing/Router";
import BaseController from "./BaseController";
/**
 * @namespace com.optrabot.ui.controller
 */
export default class TradeTemplateList extends BaseController {
	private oView: any;
	private oRouter: Router;

	public onInit(): void {
		this.oView = this.getView();
		this.oRouter = this.getOwnerComponent().getRouter();
	}

	public onTemplatePress(oEvent: any): void {
		var oFCL = this.oView.getParent().getParent();
		oFCL.setLayout("TwoColumnsMidExpanded");
		var templatePath = oEvent.getSource().getBindingContext("tradetemplates").getPath();
		var templateName = templatePath.split("/").slice(-1).pop();
		console.log("Template name: " + templateName);
		this.oRouter.navTo("template", {layout: "TwoColumnsMidExpanded", template: templateName} );
	}
}