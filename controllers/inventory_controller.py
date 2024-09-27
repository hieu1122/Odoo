from odoo import http
from odoo.http import request

class InventoryController(http.Controller):

    # Route cho Inventory Items
    @http.route('/inventory/items', auth='public', website=True)
    def inventory_items(self):
        items = request.env['inventory.item'].search([])
        return request.render('inventory_management.inventory_item_template', {
            'items': items,
        })

    # Route cho Inventory Locations
    @http.route('/inventory/locations', auth='public', website=True)
    def inventory_locations(self):
        locations = request.env['inventory.location'].search([])
        return request.render('inventory_management.inventory_location_template', {
            'locations': locations,
        })

    # Route cho Inventory Movements
    @http.route('/inventory/movements', auth='public', website=True)
    def inventory_movements(self):
        movements = request.env['inventory.movement'].search([])
        return request.render('inventory_management.inventory_movement_template', {
            'movements': movements,
        })
