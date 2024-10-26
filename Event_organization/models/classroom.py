from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ClassRoom(models.Model):
    _name = 'classroom'
    _description = 'Event classroom'

    name = fields.Char(string='Classroom Name', required=True)
    capacity = fields.Integer(string='Capacity',required=True)
    event_form_ids = fields.One2many('event.form.organization', 'room_id', string='Events')
    # Define more fields as needed

    status = fields.Selection([
        ('available', 'Available'),
        ('reserved', 'Reserved')
    ], string='Status', compute='_compute_status', store=True)


    @api.depends('event_form_ids')
    def _compute_status(self):
        for classroom in self:
            events = classroom.event_form_ids.filtered(
                lambda e: e.begin_date <= fields.Date.today() <= e.end_date
            )
            classroom.status = 'reserved' if events else 'available'


   
    def action_check_availability(self):
        view_id = self.env.ref('Event_organization.change_state_wizard_view_form').id
        return {
            'name': 'Check Availability',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'change.state',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'active_id': self.id}
        }
    
    def _check_availability(self, begin_date, end_date):
        # Check if there are any events scheduled within the specified date range
        conflicting_events = self.env['event.form.organization'].search([
            ('room_id', '=', self.id),
            '|',
            '&', ('begin_date', '<=', end_date), ('end_date', '>=', begin_date),
            '&', ('begin_date', '<=', end_date), ('end_date', '>=', begin_date)
        ])
    
        if conflicting_events:
            conflicting_event_names = ', '.join(conflicting_events.mapped('name'))
            raise ValidationError(f"The room is not available from {begin_date} to {end_date} due to the following conflicting events: {conflicting_event_names}")