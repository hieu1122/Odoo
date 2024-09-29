from odoo import models, fields

class InventoryMovement(models.Model):
    _name = 'inventory.movement'
    _description = 'Inventory Movement'

    product_id = fields.Many2one('inventory.item', string='Product', required=True)
    quantity = fields.Integer(string='Quantity', required=True)
    source_location_id = fields.Many2one('inventory.location', string='Source Location')
    destination_location_id = fields.Many2one('inventory.location', string='Destination Location')
    movement_date = fields.Datetime(string='Movement Date', default=fields.Datetime.now)
    user_id = fields.Many2one('res.users', string='User')
