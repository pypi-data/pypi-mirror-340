from ..sc_test_case import SCTestCase
from datetime import date


class CRMLeadTest(SCTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        date_invoice = date(2021, 1, 31)
        partner = self.browse_ref('easy_my_coop.res_partner_cooperator_1_demo')
        invoice = self.env['account.invoice'].create({
            'partner_id': partner.id,
            'date_invoice': date_invoice
        })
        account_invoice_model = self.env['ir.model'].search(
            [('model', '=', 'account.invoice')]
        )
        activity_type = self.ref('somconnexio.return_activity_type_1')
        self.activity = self.env['mail.activity'].create({
            'res_id': invoice.id,
            'res_model_id': account_invoice_model.id,
            'activity_type_id': activity_type,
        })

    def test_action_feedback_done_not_set(self):
        self.activity.action_feedback('')
        self.assertEquals(self.activity.date_done, date.today())

    def test_action_feedback_done_set(self):
        self.activity.date_done = '2021-01-01'
        self.activity.action_feedback('')
        self.assertEquals(self.activity.date_done, date(2021, 1, 1))

    def test_default_user_id(self):
        self.assertEquals(
            self.activity.user_id,
            self.browse_ref('base.user_admin')
        )

    def test_activity_type_id_change_keep_summary(self):
        original_summary = self.activity.summary
        new_activity_type_id = self.ref("somconnexio.return_activity_type_n")
        self.activity.activity_type_id = new_activity_type_id

        self.assertEquals(self.activity.summary, original_summary)
