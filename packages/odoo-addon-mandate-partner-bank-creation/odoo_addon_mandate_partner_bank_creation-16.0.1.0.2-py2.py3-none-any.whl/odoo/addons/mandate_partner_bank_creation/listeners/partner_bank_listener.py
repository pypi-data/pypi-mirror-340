from odoo.addons.component.core import Component


class PartnerBankListener(Component):
    _name = 'partner.bank.listener'
    _inherit = 'base.event.listener'
    _apply_on = ['res.partner.bank']

    def on_record_create(self, record, fields=None):
        if not record.partner_id.is_customer:
            return
        mandate_vals = {
            "partner_bank_id": record.id,
            "partner_id": record.partner_id.id,
            "format": "sepa",
            "type": "recurrent",
            "signature_date": record.create_date,
            "state": "valid",
        }
        self.env['account.banking.mandate'].create(mandate_vals)

