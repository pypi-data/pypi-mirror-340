import Router from "sap/ui/core/routing/Router";
import BaseController from "./BaseController";
import Page from "sap/m/Page";
/**
 * @namespace com.optrabot.ui.controller
 */
export default class TradeTemplateDetail extends BaseController {
	private oRouter: Router;
	private oControlModel: any;
	private _template: string;
	
	public onInit(): void {
		var oOwnerComponent = this.getOwnerComponent();
		this.oRouter = oOwnerComponent.getRouter();
		this.oControlModel = oOwnerComponent.getModel("control");

		this.oRouter.getRoute("template").attachPatternMatched(this._onTemplateMatched, this);
		this.oRouter.getRoute("templateWOLayout").attachPatternMatched(this._onTemplateMatched, this);
	}

	public onEditToggleButtonPress(): void {
		var oTemplatePage = this.getView().byId("TemplatePageLayout") as Page;
		var bCurrentShowFooterState = oTemplatePage.getShowFooter();
		oTemplatePage.setShowFooter(!bCurrentShowFooterState);
	}

	public _onTemplateMatched(oEvent: any): void {
		console.log("Template matched");
		this._template = oEvent.getParameter("arguments").template || this._template || "0";
		
		// Store the current template in the model
		var layout = oEvent.getParameter("arguments").layout || "TwoColumnsMidExpanded";
		this.oControlModel.setProperty("/currentLayout", layout);

		this.getView().bindElement({
			path: "/TemplateCollection/" + this._template,
			model: "tradetemplates"
		});
	}

	public onFullscreenPressed(): void {
		var sCurrentLayout = this.oControlModel.getProperty("/currentLayout");
		var sNewLayout = sCurrentLayout;
		if (sCurrentLayout === "MidColumnFullScreen") {
			sNewLayout = "TwoColumnsMidExpanded";
		} else if (sCurrentLayout === "TwoColumnsMidExpanded") {
			sNewLayout = "MidColumnFullScreen";
		}
		this.oRouter.navTo("template", {
			layout: sNewLayout, template: this._template}, true);
	}

	public onClosePressed(): void {
		this.oRouter.navTo("templates", {
			layout: "OneColumn"}, true);
	}

	public onExit(): void {
		this.oRouter.getRoute("template").detachPatternMatched(this._onTemplateMatched, this);
		this.oRouter.getRoute("templateWOLayout").detachPatternMatched(this._onTemplateMatched, this);
	}
}