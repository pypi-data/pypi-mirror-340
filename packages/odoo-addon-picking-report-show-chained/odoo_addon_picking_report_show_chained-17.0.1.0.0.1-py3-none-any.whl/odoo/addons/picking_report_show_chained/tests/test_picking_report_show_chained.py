# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.tests.common import TransactionCase


class TestPickingReportShowChained(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["res.config.settings"].write(
            {
                "group_stock_multi_locations": True,
            }
        )
        cls.warehouse = cls.env.ref("stock.warehouse0")
        cls.warehouse.delivery_steps = "pick_ship"
        cls.partner = cls.env.ref("base.res_partner_1")
        cls.procurement_group = cls.env["procurement.group"].create(
            {
                "name": "Test Procurement Group",
                "move_type": "direct",
                "partner_id": cls.partner.id,
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "product",
            }
        )
        cls.uom = cls.env.ref("uom.product_uom_unit")
        cls.pg = cls.env["procurement.group"].create({"name": "Test Procurement"})
        cls.values = {"route_ids": cls.warehouse.delivery_route_id, "group_id": cls.pg}

    def test_picking_report_show_chained(self):
        origin = "Test Origin"
        procurement = self.pg.Procurement(
            self.product,  # product_id
            1,  # product_qty
            self.uom,  # product_uom
            self.partner.property_stock_customer,  # location_id
            "Test Procurement",  # name
            origin,  # origin
            self.env.company,  # company_id
            self.values,  # values
        )
        procurements = [procurement]
        self.env["procurement.group"].run(procurements)
        picking_picking = self.env["stock.picking"].search(
            [
                ("group_id", "=", self.pg.id),
                ("picking_type_id", "=", self.warehouse.pick_type_id.id),
            ]
        )
        out_picking = self.env["stock.picking"].search(
            [
                ("group_id", "=", self.pg.id),
                ("picking_type_id", "=", self.warehouse.out_type_id.id),
            ]
        )
        self.assertEqual(len(picking_picking), 1)
        self.assertEqual(len(out_picking), 1)
        self.assertEqual(picking_picking.next_pick_id, out_picking)
        self.assertEqual(out_picking.previous_pick_ids, picking_picking)
