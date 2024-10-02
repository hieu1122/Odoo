from odoo import http
from odoo.addons.test_impex.tests.test_load import message
from odoo.http import request


class InventoryItemController(http.Controller):

    # Route cho Inventory Items
    @http.route('/inventory/item', type='http', auth='public', website=True)
    def inventory_items(self, search=None):
        domain = []
        if search:
            domain = [('name', 'ilike', search)]
        items = request.env['inventory.item'].search(domain)
        request.session['message'] = 'Invalid Name'
        return request.render('inventory_management.inventory_item_template', {
            'items': items,
            'message': request.session.get('message'),
        })

    @http.route('/inventory/item/add', type='http', auth='public', website=True)
    def inventory_item_add(self):
        return request.render('inventory_management.inventory_item_add_template')

    @http.route('/inventory/item/create', type='http', auth='public', methods=['POST'], csrf=False, website=True)
    def inventory_item_create(self, **data):
        item_name = data.get('name')
        description = data.get('description')
        quantity = data.get('quantity')
        reorder_level = data.get('reorder_level')
        if item_name:
            request.env['inventory.item'].create({
                'name': item_name,
                'description': description,
                'quantity': quantity,
                'reorder_level': reorder_level,
            })
            request.session['message'] = 'Add Item successfully.'
            return request.redirect('/inventory/item')

        request.session['message'] = 'Missing required fields'
        return request.redirect('/inventory/item')

    @http.route('/inventory/item/update/<int:item_id>', type='http', auth='public', website=True)
    def inventory_item_update(self, item_id):
        item = request.env['inventory.item'].browse(item_id)
        if item.exists():
            return request.render('inventory_management.inventory_item_update_template', {
                'item': item
            })
        else:
            request.session['message'] = 'Item not found.'
        return request.redirect('/inventory/item')

    @http.route('/inventory/item/save/<int:item_id>', type='http', auth='public', methods=['POST'], csrf=False,
                website=True)
    def inventory_item_save(self, item_id, **data):
        item = request.env['inventory.item'].browse(item_id)
        if item.exists():
            for field in ['name','description','quantity','reorder_level']:
                value = data.get(field)
                if value:
                    setattr(item, field, value)
            request.session['message'] = 'Save Item successfully.'
        else:
            request.session['message'] = 'Item not found.'
        return request.redirect('/inventory/item')

    @http.route('/inventory/item/delete/<int:item_id>', type='http', auth='public', methods=['POST'], csrf=False,
                website=True)
    def inventory_item_delete(self, item_id):
        item = request.env['inventory.item'].browse(item_id)
        if item.exists():
            item.unlink()
            request.session['message'] = 'Item deleted successfully.'
        else:
            request.session['message'] = 'Item not found.'
        return request.redirect('/inventory/item')

