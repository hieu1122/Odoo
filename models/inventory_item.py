from odoo import models, fields

class InventoryItem(models.Model):
    _name = 'inventory.item'
    _description = 'Inventory Item'

    item_id=fields.Many2one('inventory.item')
    name = fields.Char(string='Item Name', required=True)
    description = fields.Text(string='Description')
    quantity = fields.Integer(string='Quantity', required=True, default=0)
    unit_of_measure = fields.Char(string='Unit of Measure')
    reorder_level = fields.Integer(string='Reorder Level')
    user_id=fields.Many2one('res.users', string='User')
