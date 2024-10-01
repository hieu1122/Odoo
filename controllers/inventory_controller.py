from odoo import http
from odoo.http import request


class InventoryController(http.Controller):

    # Route cho Inventory Items
    @http.route('/inventory/item', type='http', auth='public', website=True)
    def inventory_items(self):
        items = request.env['inventory.item'].search([])
        message = request.session.pop('message', False)
        return request.render('inventory_management.inventory_item_template', {
            'items': items,
            'message': message,
        })

    @http.route('/inventory/item/add', type='http', auth='public', website=True)
    def inventory_items_add(self):
        return request.render('inventory_management.inventory_item_add_template')

    @http.route('/inventory/item/create', type='http', auth='public', methods=['POST'], csrf=False)
    def inventory_items_create(self, **post):
        item_name = post.get('name')
        description = post.get('description')
        quantity = post.get('quantity')
        reorder_level = post.get('reorder_level')
        if item_name and quantity is not None:
            request.env['inventory.item'].create({
                'name': item_name,
                'description': description,
                'quantity': quantity,
                'reorder_level': reorder_level,
            })
            request.session['message'] = 'Add Item successfully.'
            return request.redirect('/inventory/item')
        return request.make_response('Missing required fields', status=400)

    @http.route('/inventory/item/update/<int:item_id>', type='http', auth='public', website=True)
    def inventory_items_update(self, item_id):
        item = request.env['inventory.item'].browse(item_id)
        if item.exists():
            return request.render('inventory_management.inventory_item_update_template', {
                'item': item
            })
        else:
            request.session['message'] = 'Item not found.'
        return request.redirect('/inventory/item')


    @http.route('/inventory/item/save/<int:item_id>', type='http', auth='public', methods=['POST'], csrf=False)
    def inventory_items_save(self, item_id, **post):
        item = request.env['inventory.item'].browse(item_id)
        if item.exists():
            item_name = post.get('name')
            item_description = post.get('description')
            item_quantity = post.get('quantity')
            item_reorder_level = post.get('reorder_level')

            if item_name is not None:
                item.name = item_name
            if item_description is not None:
                item.description = item_description
            if item_quantity is not None:
                item.quantity = int(item_quantity)
            if item_reorder_level is not None:
                item.reorder_level = int(item_reorder_level)
            request.session['message'] = 'Update Item successfully.'
        else:
            request.session['message'] = 'Item not found.'
        return request.redirect('/inventory/item')


    @http.route('/inventory/item/delete/<int:item_id>', type='http', auth='public', methods=['POST'], csrf=False)
    def inventory_items_delete(self, item_id):
        item = request.env['inventory.item'].browse(item_id)
        if item.exists():
            item.unlink()
            request.session['message'] = 'Item deleted successfully.'
        else:
            request.session['message'] = 'Item not found.'
        return request.redirect('/inventory/item')

    # Route cho Inventory Locations
    @http.route('/inventory/locations', type='http', auth='public', website=True)
    def inventory_locations(self):
        locations = request.env['inventory.location'].search([])
        return request.render('inventory_management.inventory_location_template', {
            'locations': locations,
        })

    # Route cho Inventory Movements
    @http.route('/inventory/movements', type='http', auth='public', website=True)
    def inventory_movements(self):
        movements = request.env['inventory.movement'].search([])
        return request.render('inventory_management.inventory_movement_template', {
            'movements': movements,
        })
