from mock import Mock, call, patch

from ..helper_service import crm_lead_create
from ..sc_test_case import SCTestCase
from odoo.exceptions import ValidationError


class CRMLeadLineTest(SCTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.partner_id = self.browse_ref("somconnexio.res_partner_2_demo")
        self.partner_iban = self.partner_id.bank_ids[0].sanitized_acc_number

        self.crm_lead_line_args = {
            "name": "666666666",
            "product_id": "666666666",
            "mobile_isp_info": None,
            "broadband_isp_info": None,
            "iban": self.partner_iban,
        }

        self.mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'new',
        })
        self.broadband_isp_info = self.env['broadband.isp.info'].create({
            'phone_number': '666666666',
            'type': 'new',
        })

        broadband_adsl_product_tmpl_args = {
            'name': 'ADSL 20Mb',
            'type': 'service',
            'categ_id': self.ref('somconnexio.broadband_adsl_service')
        }
        product_adsl_broadband_tmpl = self.env['product.template'].create(
            broadband_adsl_product_tmpl_args
        )
        self.product_broadband_adsl = product_adsl_broadband_tmpl.product_variant_id
        broadband_fiber_product_tmpl_args = {
            'name': 'Fiber 100Mb',
            'type': 'service',
            'categ_id': self.ref('somconnexio.broadband_fiber_service')
        }
        product_fiber_broadband_tmpl = self.env['product.template'].create(
            broadband_fiber_product_tmpl_args
        )
        self.product_broadband_fiber = product_fiber_broadband_tmpl.product_variant_id

        mobile_product_tmpl_args = {
            'name': 'Sense minutes',
            'type': 'service',
            'categ_id': self.ref('somconnexio.mobile_service'),
            'attribute_ids': [(4, self.ref('somconnexio.InPack'))],
        }
        product_mobile_tmpl = self.env['product.template'].create(
            mobile_product_tmpl_args
        )
        self.product_mobile = product_mobile_tmpl.product_variant_id
        self.product_pack_mobile = self.env['product.product'].create({
            'product_tmpl_id': product_mobile_tmpl.id,
            'attribute_value_ids': [(4, self.ref('somconnexio.IsInPack'))]
        })

    def test_mobile_lead_line_creation_ok(self):
        crm_lead_line_args_copy = self.crm_lead_line_args.copy()
        crm_lead_line_args_copy.update({
            'mobile_isp_info': self.mobile_isp_info.id,
            'product_id': self.product_mobile.id
        })

        mobile_crm_lead_line = self.env['crm.lead.line'].create(
            [crm_lead_line_args_copy]
        )
        self.assertTrue(mobile_crm_lead_line.id)
        self.assertTrue(mobile_crm_lead_line.is_mobile)
        self.assertFalse(mobile_crm_lead_line.is_from_pack)
        self.assertEquals(mobile_crm_lead_line.iban, self.partner_iban)
        self.assertEquals(mobile_crm_lead_line.create_reason, self.mobile_isp_info.type)

    def test_broadband_lead_line_creation_ok(self):
        crm_lead_line_args_copy = self.crm_lead_line_args.copy()
        crm_lead_line_args_copy.update({
            'broadband_isp_info': self.broadband_isp_info.id,
            'product_id': self.product_broadband_adsl.id
        })

        broadband_crm_lead_line = self.env['crm.lead.line'].create(
            [crm_lead_line_args_copy]
        )
        self.assertTrue(broadband_crm_lead_line.id)
        self.assertTrue(broadband_crm_lead_line.is_adsl)
        self.assertEquals(broadband_crm_lead_line.iban, self.partner_iban)
        self.assertEquals(
            broadband_crm_lead_line.create_reason, self.broadband_isp_info.type
        )

    def test_broadband_4G_lead_line_creation_ok(self):
        self.broadband_isp_info.update({"phone_number": "-"})
        crm_lead_line_args_copy = self.crm_lead_line_args.copy()
        crm_lead_line_args_copy.update({
            'broadband_isp_info': self.broadband_isp_info.id,
            'product_id': self.env.ref('somconnexio.Router4G').id
        })

        broadband_crm_lead_line = self.env['crm.lead.line'].create(
            [crm_lead_line_args_copy]
        )
        self.assertTrue(broadband_crm_lead_line.id)
        self.assertTrue(broadband_crm_lead_line.is_4G)
        self.assertEquals(
            broadband_crm_lead_line.create_reason, self.broadband_isp_info.type
        )

    def test_broadband_lead_line_creation_without_broadband_isp_info(self):
        crm_lead_line_args_copy = self.crm_lead_line_args.copy()
        crm_lead_line_args_copy.update({
            'product_id': self.product_broadband_adsl.id
        })

        self.assertRaises(
            ValidationError,
            self.env['crm.lead.line'].create,
            [crm_lead_line_args_copy]
        )

    def test_mobile_lead_line_creation_without_mobile_isp_info(self):
        crm_lead_line_args_copy = self.crm_lead_line_args.copy()
        crm_lead_line_args_copy.update({
            'product_id': self.product_mobile.id
        })

        self.assertRaises(
            ValidationError,
            self.env['crm.lead.line'].create,
            [crm_lead_line_args_copy]
        )

    def test_broadband_check_phone_number_on_change(self):
        crm_lead_line_args_copy = self.crm_lead_line_args.copy()
        crm_lead_line_args_copy.update({
            'broadband_isp_info': self.broadband_isp_info.id,
            'product_id': self.product_broadband_adsl.id,
        })
        ba_crm_lead_line = self.env['crm.lead.line'].create(
            [crm_lead_line_args_copy]
        )
        self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'lead_line_ids': [(6, 0, [ba_crm_lead_line.id])],
                'stage_id': self.env.ref("crm.stage_lead1").id,
            }]
        )
        self.assertFalse(ba_crm_lead_line.lead_id.skip_duplicated_phone_validation)
        ba_crm_lead_line.check_phone_number = True
        ba_crm_lead_line._onchange_check_phone_number()
        self.assertTrue(ba_crm_lead_line.lead_id.skip_duplicated_phone_validation)

    @patch(
        "odoo.addons.somconnexio.models.crm_lead_line.CRMLeadLine.update_ticket_with_coverage_info",  # noqa
    )
    @patch(
        "odoo.addons.somconnexio.models.crm_lead_line.CustomerDataFromResPartner"  # noqa
    )
    @patch(
        "odoo.addons.somconnexio.otrs_factories.ticket_service_data.TicketServiceData.build"  # noqa
    )
    @patch("odoo.addons.somconnexio.models.crm_lead_line.TicketFactory")
    def test_create_ticket(
        self,
        MockTicketFactory,
        mock_service_data_build,
        MockCustomerData,
        mock_update_ticket,
    ):
        crm_lead = crm_lead_create(
            self.env,
            self.partner_id,
            "mobile",
        )
        crm_lead_line = crm_lead.lead_line_ids[0]

        mock_service_data_build.return_value = "mock_service_data"
        MockCustomerData.return_value.build.return_value = "mock_customer_data"
        mock_ticket = Mock(spec_set=["create", "id", "number"])
        mock_ticket.id = 123
        mock_ticket.number = "123456"
        MockTicketFactory.return_value.build.return_value = mock_ticket

        crm_lead_line.create_ticket()

        MockCustomerData.assert_called_once_with(self.partner_id)
        MockCustomerData.return_value.build.assert_called_once()
        MockTicketFactory.assert_called_once_with(
            "mock_service_data", "mock_customer_data"
        )
        MockTicketFactory.return_value.build.assert_called_once()
        mock_ticket.create.assert_called_once()

        self.assertEquals(crm_lead_line.ticket_number, mock_ticket.number)
        mock_update_ticket.assert_called_once_with(mock_ticket.id)

    @patch(
        'odoo.addons.somconnexio.models.crm_lead_line.UpdateProcessTicketWithCoverageTicketsInfoService',  # noqa
    )
    def test_update_broadband_ticket_with_coverage_info(self, MockUpdateTicketService):
        crm_lead = self.env["crm.lead"].create(
            [
                {
                    "name": "Test Lead",
                    "partner_id": self.partner_id.id,
                }
            ]
        )
        provision_ticket_id = 123

        crm_lead_line_args_copy = self.crm_lead_line_args.copy()
        crm_lead_line_args_copy.update(
            {
                "lead_id": crm_lead.id,
                "broadband_isp_info": self.broadband_isp_info.id,
                "product_id": self.product_broadband_adsl.id,
            }
        )

        broadband_crm_lead_line = self.env['crm.lead.line'].create(
            [crm_lead_line_args_copy]
        )

        mock_update_ticket_service = Mock(spec=['run'])

        def mock_update_ticket_service_side_effect(ticket_id):
            if ticket_id == provision_ticket_id:
                return mock_update_ticket_service

        MockUpdateTicketService.side_effect = mock_update_ticket_service_side_effect

        broadband_crm_lead_line.update_ticket_with_coverage_info(provision_ticket_id)

        mock_update_ticket_service.run.assert_has_calls([
            call('sara.merna@smerna.net'),
            call('sara.merna@demo.net'),
        ])

    @patch(
        'odoo.addons.somconnexio.models.crm_lead_line.UpdateProcessTicketWithCoverageTicketsInfoService',  # noqa
    )
    def test_update_mobile_ticket_with_coverage_info(self, MockUpdateTicketService):
        crm_lead = self.env["crm.lead"].create(
            [
                {
                    "name": "Test Lead",
                    "partner_id": self.partner_id.id,
                }
            ]
        )
        provision_ticket_id = 123

        crm_lead_line_args_copy = self.crm_lead_line_args.copy()
        crm_lead_line_args_copy.update(
            {
                "lead_id": crm_lead.id,
                "mobile_isp_info": self.mobile_isp_info.id,
                "product_id": self.product_mobile.id,
            }
        )
        mobile_crm_lead_line = self.env["crm.lead.line"].create(
            [crm_lead_line_args_copy]
        )
        mobile_crm_lead_line.update_ticket_with_coverage_info(provision_ticket_id)

        MockUpdateTicketService.assert_not_called()

    def test_update_mobile_isp_info_has_sim(self):
        crm_lead = self.env["crm.lead"].create(
            [{"name": "Test Lead", "partner_id": self.partner_id.id}]
        )
        crm_lead_line_args_copy = self.crm_lead_line_args.copy()
        crm_lead_line_args_copy.update(
            {
                "lead_id": crm_lead.id,
                "mobile_isp_info": self.mobile_isp_info.id,
                "product_id": self.product_mobile.id,
            }
        )
        mobile_crm_lead_line = self.env["crm.lead.line"].create(
            [crm_lead_line_args_copy]
        )
        self.assertFalse(self.mobile_isp_info.has_sim)
        mobile_crm_lead_line.mobile_isp_info_has_sim = True
        self.assertTrue(self.mobile_isp_info.has_sim)

    def test_mobile_pack_lead_line_creation_ok(self):
        crm_lead_line_args_copy = self.crm_lead_line_args.copy()
        crm_lead_line_args_copy.update({
            'mobile_isp_info': self.mobile_isp_info.id,
            'product_id': self.product_pack_mobile.id
        })

        mobile_crm_lead_line = self.env['crm.lead.line'].create(
            [crm_lead_line_args_copy]
        )
        self.assertTrue(mobile_crm_lead_line.id)
        self.assertTrue(mobile_crm_lead_line.is_mobile)
        self.assertTrue(mobile_crm_lead_line.is_from_pack)
