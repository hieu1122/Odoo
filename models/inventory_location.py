from odoo import models, fields

class InventoryLocation(models.Model):
    _name = 'inventory.location'
    _description = 'Inventory Location'

    name = fields.Char(string='Location Name', required=True)
    address = fields.Char(string='Address')
    capacity = fields.Integer(string='Capacity')
    user_id=fields.Many2one('res.users', string='User')
