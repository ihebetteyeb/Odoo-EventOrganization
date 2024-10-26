from odoo import fields, models, api


class ChangeState(models.TransientModel):
    _name = 'change.state'

    classroom_id = fields.Many2one('classroom')
    state = fields.Selection([
         ('available', 'Available'),
        ('reserved', 'Reserved')
    ],default="available")
    begin_date = fields.Date(string='Begin Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    
  
    def action_confirm(self):
        self.ensure_one()
        classroom_id = self.env.context.get('active_id')
        classroom = self.env['classroom'].browse(classroom_id)
        classroom._check_availability(self.begin_date, self.end_date)
        # Add any additional logic here
        return {'type': 'ir.actions.act_window_close'}
