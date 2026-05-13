# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.depends("sale_line_id", "sale_line_id.product_id")
    def _compute_sale_line_product_id(self):
        for task in self:
            if task.sale_line_id and task.sale_line_id.product_id:
                task.sale_line_product_id = task.sale_line_id.product_id.id
            else:
                task.sale_line_product_id = False

    @api.depends("sale_line_id", "sale_line_id.product_uom_qty")
    def _compute_sale_line_product_uom_qty(self):
        for task in self:
            if task.sale_line_id:
                task.sale_line_product_uom_qty = task.sale_line_id.product_uom_qty
            else:
                task.sale_line_product_uom_qty = 0

    @api.depends("sale_line_id", "sale_line_id.price_unit")
    def _compute_sale_line_sale_price(self):
        for task in self:
            if task.sale_line_id:
                task.product_uom_id = task.sale_line_id.product_uom.id
                task.sale_line_sale_price = task.sale_line_id.price_unit
            else:
                task.sale_line_sale_price = 0

    @api.depends("sale_line_product_uom_qty", "sale_line_sale_price")
    def _compute_sale_subtotal(self):
        for task in self:
            task.sale_subtotal = (
                task.sale_line_product_uom_qty * task.sale_line_sale_price
            )

    @api.depends(
        "sale_line_product_uom_qty", "sale_line_sale_price", "product_standard_price"
    )
    def _compute_totals(self):
        for task in self:
            sale_subtotal = task.sale_line_product_uom_qty * task.sale_line_sale_price
            total_cost = task.sale_line_product_uom_qty * task.product_standard_price
            task.sale_subtotal = sale_subtotal
            task.total_cost = total_cost
            task.profit = sale_subtotal - total_cost

    sale_line_product_id = fields.Many2one(
        string="Sale line product",
        comodel_name="product.product",
        related=False,
        compute="_compute_sale_line_product_id",
        store=True,
        readonly=False,
    )
    sale_line_product_category_id = fields.Many2one(
        string="Sale Line Product Category",
        comodel_name="product.category",
        related="sale_line_product_id.categ_id",
        store=True,
    )
    sale_line_product_uom_qty = fields.Float(
        string="Sale line quantity",
        digits="Product Unit of Measure",
        related=False,
        compute="_compute_sale_line_product_uom_qty",
        store=True,
        readonly=False,
    )
    product_uom_category_id = fields.Many2one(
        related="sale_line_product_id.uom_id.category_id",
        depends=["sale_line_product_id"],
    )
    product_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Unit of Measure",
        compute="_compute_sale_line_product_uom_qty",
        store=True,
        readonly=False,
        domain="[('category_id', '=', product_uom_category_id)]",
    )

    sale_line_sale_price = fields.Float(
        string="Sale line sale price",
        min_display_digits="Product Price",
        compute="_compute_sale_line_sale_price",
        store=True,
        readonly=False,
    )
    product_standard_price = fields.Float(
        string="Product Cost",
        company_dependent=True,
        min_display_digits="Product Price",
    )
    sale_subtotal = fields.Float(
        compute="_compute_totals",
        min_display_digits="Product Price",
        store=True,
        readonly=True,
    )
    total_cost = fields.Float(
        compute="_compute_totals",
        min_display_digits="Product Price",
        store=True,
        readonly=True,
    )
    profit = fields.Float(
        compute="_compute_totals",
        min_display_digits="Product Price",
        store=True,
        readonly=True,
    )

    @api.onchange("sale_line_product_id")
    def _onchange_sale_line_product_id(self):
        if self.sale_line_product_id:
            self.product_standard_price = self.sale_line_product_id.standard_price
            if (
                not self.sale_line_id
                or self.sale_line_id.price_unit != self.sale_line_sale_price
                or self.sale_line_product_id != self.sale_line_id.product_id
            ):
                self.sale_line_sale_price = self.sale_line_product_id.list_price
                self.product_uom_id = self.sale_line_product_id.uom_id.id

    @api.onchange("sale_line_id")
    def _onchange_sale_line_id(self):
        if not self.sale_line_id:
            self.product_uom_id = False
            self.product_standard_price = 0
