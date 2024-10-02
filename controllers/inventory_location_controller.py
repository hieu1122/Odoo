from odoo import http
from odoo.http import request


class InventoryLocationController(http.Controller):
    # Route cho Inventory Locations
    @http.route('/inventory/location', type='http', auth='public', website=True)
    def inventory_locations(self, search=None):
        domain = []
        if search:
            domain = [('name', 'ilike', search)]
        locations = request.env['inventory.location'].search(domain)
        message = request.session.pop('message', False)
        return request.render('inventory_management.inventory_location_template', {
            'locations': locations,
            'message': message,
        })

    @http.route('/inventory/location/add', type='http', auth='public', website=True)
    def inventory_location_add(self):
        return request.render('inventory_management.inventory_location_add_template')

    @http.route('/inventory/location/create', type='http', auth='public', methods=['POST'], csrf=False, website=True)
    def inventory_location_create(self, **data):
        if all(data.get(field) for field in ['name', 'address', 'capacity']):
            request.env['inventory.location'].create({
                'name': data['name'],
                'address': data['address'],
                'capacity': data['capacity'],
            })
            request.session['message'] = 'Location added successfully.'
            return request.redirect('/inventory/location')
        return request.make_response('Missing required fields', status=400)

    @http.route('/inventory/location/update/<int:location_id>', type='http', auth='public', website=True)
    def inventory_location_update(self, location_id):
        location = request.env['inventory.location'].browse(location_id)
        if location.exists():
            return request.render('inventory_management.inventory_location_update_template', {
                'location': location
            })
        else:
            request.session['message'] = 'Location not found.'
        return request.redirect('/inventory/location')

    @http.route('/inventory/location/save/<int:location_id>', type='http', auth='public', methods=['POST'], csrf=False,
                website=True)
    def inventory_location_save(self, location_id, **data):
        location = request.env['inventory.location'].browse(location_id)
        if location.exists():
            for field in ['name', 'address', 'capacity']:
                value = data.get(field)
                if value:
                    setattr(location, field, value)
            request.session['message'] = 'Update Location successfully.'
        else:
            request.session['message'] = 'Location not found.'
        return request.redirect('/inventory/location')

    @http.route('/inventory/location/delete/<int:location_id>', type='http', auth='public', methods=['POST'], csrf=False,
                website=True)
    def inventory_location_delete(self, location_id):
        location = request.env['inventory.location'].browse(location_id)
        if location.exists():
            location.unlink()
            request.session['message'] = 'Delete Location successfully.'
        else:
            request.session['message'] = 'Location not found.'
        return request.redirect('/inventory/location')
