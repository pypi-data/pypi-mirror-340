from mock import patch, Mock, ANY
import odoo
import json
from odoo.addons.easy_my_coop_api.tests.common import BaseEMCRestCase
from odoo.exceptions import UserError
from ...services.contract_email_change_process import ContractEmailChangeProcess
from datetime import date
from ..helper_service import contract_fiber_create_data

HOST = "127.0.0.1"
PORT = odoo.tools.config["http_port"]


class BaseEMCRestCaseAdmin(BaseEMCRestCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        # Skip parent class in super to avoid recreating api key
        super(BaseEMCRestCase, cls).setUpClass(*args, **kwargs)
        cls.env = cls.env(context=dict(
            cls.env.context,
            tracking_disable=True,  # no jobs thanks
        ))


class TestContractEmailChangeService(BaseEMCRestCaseAdmin):
    def setUp(self, *args, **kwargs):
        super().setUp()
        self.partner = self.browse_ref("somconnexio.res_partner_2_demo")
        self.partner.ref = "1234test"
        self.partner_ref = self.partner.ref
        self.email = "test@example.org"
        self.ResPartner = self.env['res.partner']
        self.partner_email_b = self.ResPartner.create({
            'name': 'Email b',
            'email': self.email,
            'type': 'contract-email',
            'parent_id': self.partner.id
        })
        vals_contract = contract_fiber_create_data(self.env, self.partner)
        self.Contract = self.env['contract.contract']
        self.contract = self.Contract.create(vals_contract)
        vals_contract_same_partner = vals_contract.copy()
        vals_contract_same_partner.update({
            'name': 'Test Contract Broadband B',
            "code": "1234b"
        })
        self.contract_same_partner = self.Contract.create(
            vals_contract_same_partner
        )
        self.user_admin = self.browse_ref('base.user_admin')
        self.expected_activity_args = {
            'res_model_id': self.env.ref('contract.model_contract_contract').id,
            'user_id': 1,
            'activity_type_id': self.env.ref('somconnexio.mail_activity_type_contract_data_change').id,  # noqa
            'date_done': date.today(),
            'date_deadline': date.today(),
            'summary': 'Email change',
            'done': True,
        }

    def http_public_post(self, url, data, headers=None):
        if url.startswith("/"):
            url = "http://{}:{}{}".format(HOST, PORT, url)
        return self.session.post(url, json=data)

    @patch(
        'odoo.addons.somconnexio.wizards.partner_email_change.partner_email_change.ChangePartnerEmails',  # noqa
        return_value=Mock(spec=[
            "change_contracts_emails",
        ])
    )
    def test_route_right_run_wizard_contract_emails_change(self, MockChangePartnerEmails):  # noqa
        url = "/public-api/contract-email-change"
        data = {
            "partner_id": self.partner_ref,
            "email": self.email,
            "contracts": {},
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractEmailChangeProcess(self.env)
        process.run_from_api(**data)
        MockChangePartnerEmails.assert_called_once_with(
            ANY,
            self.partner
        )
        MockChangePartnerEmails.return_value.change_contracts_emails.assert_called_once_with(  # noqa
            self.Contract.browse([self.contract_same_partner.id, self.contract.id]),
            self.ResPartner.browse(self.partner_email_b.id),
            self.expected_activity_args,
            contract_group_id=self.env["contract.group"],
            create_contract_group=True,
        )

    @patch(
        'odoo.addons.somconnexio.wizards.partner_email_change.partner_email_change.ChangePartnerEmails',  # noqa
        return_value=Mock(spec=[
            "change_contracts_emails",
        ])
    )
    def test_route_right_run_wizard_one_contract_emails_change(self, MockChangePartnerEmails):  # noqa
        url = "/public-api/contract-email-change"
        data = {
            "partner_id": self.partner_ref,
            "email": self.email,
            "contracts": self.contract.code
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractEmailChangeProcess(self.env)
        process.run_from_api(**data)
        MockChangePartnerEmails.assert_called_once_with(
            ANY,
            self.partner
        )
        MockChangePartnerEmails.return_value.change_contracts_emails.assert_called_once_with(  # noqa
            self.Contract.browse(self.contract.id),
            self.ResPartner.browse(self.partner_email_b.id),
            self.expected_activity_args,
            contract_group_id=self.env["contract.group"],
            create_contract_group=True,
        )

    @patch(
        'odoo.addons.somconnexio.wizards.partner_email_change.partner_email_change.ChangePartnerEmails',  # noqa
        return_value=Mock(spec=[
            "change_contracts_emails",
        ])
    )
    def test_route_right_run_wizard_many_contracts_emails_change(self, MockChangePartnerEmails):  # noqa
        url = "/public-api/contract-email-change"
        data = {
            "partner_id": self.partner_ref,
            "email": self.email,
            "contracts": "{};{}".format(
                self.contract.code, self.contract_same_partner.code
            )
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractEmailChangeProcess(self.env)
        process.run_from_api(**data)
        MockChangePartnerEmails.assert_called_once_with(
            ANY,
            self.partner
        )
        MockChangePartnerEmails.return_value.change_contracts_emails.assert_called_once_with(  # noqa
            self.Contract.browse([self.contract.id, self.contract_same_partner.id]),
            self.ResPartner.browse(self.partner_email_b.id),
            self.expected_activity_args,
            contract_group_id=self.env["contract.group"],
            create_contract_group=True,
        )

    def test_route_bad_run_wizard_contract_code_not_found(self):
        url = "/public-api/contract-email-change"
        data = {
            "partner_id": self.partner_ref,
            "email": self.email,
            "contracts": "XXX",
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractEmailChangeProcess(self.env)
        self.assertRaises(
            UserError,
            process.run_from_api,
            **data
        )

    def test_create_email_partner(self):
        email = "test123@example.org"
        process = ContractEmailChangeProcess(self.env)
        partner = process._create_email_partner(self.partner, email)
        self.assertEquals(partner.parent_id, self.partner)
        self.assertEquals(partner.email, email)
        self.assertEquals(partner.type, 'contract-email')

    @patch(
        'odoo.addons.somconnexio.wizards.partner_email_change.partner_email_change.ChangePartnerEmails',  # noqa
        return_value=Mock(spec=[
            "change_contracts_emails",
        ])
    )
    def test_route_right_run_wizard_email_not_found(self, MockChangePartnerEmails):  # noqa
        email = "test123@example.org"
        url = "/public-api/contract-email-change"
        data = {
            "partner_id": self.partner_ref,
            "email": email,
            "contracts": {},
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractEmailChangeProcess(self.env)
        process.run_from_api(**data)
        MockChangePartnerEmails.assert_called_once_with(
            ANY,
            self.partner
        )
        new_email = self.env['res.partner'].search([
            ('parent_id', '=', self.partner.id),
            ('email', '=', email),
            ('type', '=', 'contract-email')
        ])
        MockChangePartnerEmails.return_value.change_contracts_emails.assert_called_once_with(  # noqa
            self.Contract.browse([self.contract.id, self.contract_same_partner.id]),
            new_email,
            self.expected_activity_args,
            contract_group_id=self.env["contract.group"],
            create_contract_group=True,
        )

    def test_route_bad_run_wizard_missing_partner_id(self):
        url = "/public-api/contract-email-change"
        data = {
            "email": self.email,
            "contracts": {},
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractEmailChangeProcess(self.env)
        self.assertRaises(
            UserError,
            process.run_from_api,
            **data
        )

    def test_route_bad_run_wizard_missing_email(self):
        url = "/public-api/contract-email-change"
        data = {
            "partner_id": self.partner_ref,
            "contracts": {},
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractEmailChangeProcess(self.env)
        self.assertRaises(
            UserError,
            process.run_from_api,
            **data
        )

    def test_route_bad_run_wizard_partner_id_not_found(self):
        url = "/public-api/contract-email-change"
        data = {
            "partner_id": 'XXX',
            "email": self.email,
            "contracts": {},
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractEmailChangeProcess(self.env)
        self.assertRaises(
            UserError,
            process.run_from_api,
            **data
        )

    def test_route_bad_run_wizard_contracts_missing(self):
        url = "/public-api/contract-email-change"
        data = {
            "partner_id": self.partner_ref,
            "email": self.email,
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractEmailChangeProcess(self.env)
        self.assertRaises(
            UserError,
            process.run_from_api,
            **data
        )

    def test_route_bad_run_wizard_contracts_dict(self):
        url = "/public-api/contract-email-change"
        data = {
            "partner_id": self.partner_ref,
            "email": self.email,
            "contracts": {"a": "b"}
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractEmailChangeProcess(self.env)
        self.assertRaises(
            UserError,
            process.run_from_api,
            **data
        )
