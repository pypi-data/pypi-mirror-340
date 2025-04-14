# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    next_pick_id = fields.Many2one(
        comodel_name="stock.picking",
        string="Picking Pick",
        compute="_compute_next_pick_id",
    )
    previous_pick_ids = fields.One2many(
        comodel_name="stock.picking",
        string="Previous Pick",
        inverse_name="next_pick_id",
        compute="_compute_previous_pick_ids",
    )
    related_pick_ids = fields.Many2many(
        comodel_name="stock.picking",
        compute="_compute_next_pick_id",
        relation="related_pick_ids_rel",
    )

    def _compute_previous_pick_ids(self):
        for sel in self:
            previous_pick_ids = []
            move_ids = sel.move_ids
            related_move_ids = self.env["stock.move"].search(
                [
                    ("move_dest_ids", "in", move_ids.ids),
                ]
            )
            if related_move_ids:
                previous_pick_ids = (
                    related_move_ids.mapped("picking_id")
                    .filtered(lambda a: a.state != "cancel")
                    .ids
                )
            sel.previous_pick_ids = [(6, 0, previous_pick_ids)]

    def _compute_next_pick_id(self):
        customers_location = self.env.ref("stock.stock_location_customers")
        outgoing_picking_type = self.env.ref("stock.picking_type_out")
        for sel in self:
            location_dest_ids = sel.mapped("move_ids.location_dest_id")
            next_pick_id = False
            related_pick_ids = []
            if (
                location_dest_ids
                and location_dest_ids[0] != customers_location
                and sel.mapped("move_ids.move_dest_ids")
                and sel.mapped("move_ids.move_dest_ids")[0].picking_id.picking_type_id
                == outgoing_picking_type
            ):
                next_pick_id = sel.mapped("move_ids.move_dest_ids")[0].picking_id
                if next_pick_id.state != "cancel":
                    next_pick_move_ids = next_pick_id.move_ids
                    related_move_ids = self.env["stock.move"].search(
                        [
                            ("move_dest_ids", "in", next_pick_move_ids.ids),
                        ]
                    )
                    if related_move_ids:
                        related_pickings = related_move_ids.mapped(
                            "picking_id"
                        ).filtered(lambda a: a.state != "cancel")
                        related_pick_ids = (related_pickings - sel).ids
            sel.next_pick_id = next_pick_id.id if next_pick_id else False
            sel.related_pick_ids = related_pick_ids
