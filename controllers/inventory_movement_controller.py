
from odoo import http
from datetime import datetime
from odoo.http import request


class InventoryMovementController(http.Controller):
    @http.route('/inventory/movement', type='http', auth='public', website=True)
    def inventory_movement(self,search=None):
        domain=[]
        if search:
            location_ids = request.env['inventory.location'].search([('name', 'ilike', search)]).ids
            domain = [('source_location_id', 'in', location_ids), ('destination_location_id', 'in', location_ids)]
        movements=request.env['inventory.movement'].search(domain)
        locations=request.env['inventory.location'].search([])
        return request.render('inventory_management.inventory_movement_template', {
            'movements':movements,
            'locations':locations,
        })

    @http.route('/inventory/movement/add', type='http', auth='public', website=True)
    def inventory_movement_add(self):
        locations = request.env['inventory.location'].search([])
        return request.render('inventory_management.inventory_movement_add_template',{
            'locations':locations
        })

    @http.route('/inventory/movement/create', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def inventory_movement_create(self,**data):
        if all(data.get(field) for field in ['quantity','source_location_id','destination_location_id','movement_date']):
            movement_date_str = data['movement_date']
            movement_date = datetime.strptime(movement_date_str, '%Y-%m-%dT%H:%M')
            request.env['inventory.movement'].create({
                'quantity':data['quantity'],
                'source_location_id':data['source_location_id'],
                'destination_location_id':data['destination_location_id'],
                'movement_date':movement_date,
            })
            request.session['message'] = 'Movement added successfully.'
            return request.redirect('/inventory/movement')
        return request.make.response('False',status=404)

    @http.route('/inventory/movement/update/<int:movement_id>', type='http', auth='public', website=True)
    def inventory_movement_update(self, movement_id):
        movement = request.env['inventory.movement'].browse(movement_id)
        locations = request.env['inventory.location'].search([])
        return request.render('inventory_management.inventory_movement_update_template', {
            'movement': movement,
            'locations': locations,
        })


    @http.route('/inventory/movement/save/<int:movement_id>', type='http', auth='public', website=True,
                methods=['POST'], csrf=False)
    def inventory_movement_save(self, movement_id, **data):
        movement = request.env['inventory.movement'].browse(movement_id)

        # Hàm phụ: Lấy ID của địa điểm (dùng nếu có)
        def get_location_id(location_data):
            location = request.env['inventory.location'].browse(int(location_data)) if location_data.isdigit() else \
            request.env['inventory.location'].search([('name', '=', location_data)], limit=1)
            return location.id if location else False

        # Chuẩn bị dữ liệu cập nhật
        update_values = {
            'quantity': data.get('quantity'),
            'source_location_id': get_location_id(data.get('source_location_id')),
            'destination_location_id': get_location_id(data.get('destination_location_id')),
            'movement_date': data.get('movement_date')
        }

        try:
            # Chuyển đổi ngày giờ nếu có
            if update_values['movement_date']:
                update_values['movement_date'] = datetime.strptime(update_values['movement_date'], '%Y-%m-%dT%H:%M')
        except ValueError:
            request.session['message'] = 'Invalid date format.'
            return request.redirect('/inventory/movement')

        # Loại bỏ các giá trị None hoặc rỗng
        update_values = {k: v for k, v in update_values.items() if v}

        # Cập nhật bản ghi nếu có giá trị mới
        if update_values:
            movement.write(update_values)
            request.session['message'] = 'Save Movement successfully.'
        else:
            request.session['message'] = 'No changes to update.'

        return request.redirect('/inventory/movement')

    @http.route('/inventory/movement/delete/<int:movement_id>', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def inventory_movement_delete(self,movement_id):
        movement = request.env['inventory.movement'].browse(movement_id)
        if movement.exists():
            movement.unlink()
            request.session['message'] = 'Delete Location successfully.'
        else:
            request.session['message'] = 'Location not found.'
        return request.redirect('/inventory/movement')


