import json
from ..common_service import BaseEMCRestCaseAdmin
from datetime import datetime, timedelta, date
import odoo

from ...services.vat_normalizer import VATNormalizer


class SubscriptionRequestServiceRestCase(BaseEMCRestCaseAdmin):
    def setUp(self):
        super().setUp()
        self.vals_subscription = {
            "name": "Manuel Dublues Test",
            "firstname": "Manuel",
            "lastname": "Dublues Test",
            "email": "manuel@demo-test.net",
            "address": {
                "street": "Fuenlabarada",
                "zip_code": "28943",
                "city": "Madrid",
                "country": "ES",
                "state": self.browse_ref("base.state_es_m").code,
            },
            "city": "Brussels",
            "zip_code": "1111",
            "country_id": self.ref("base.es"),
            "date": (datetime.now() - timedelta(days=12)).strftime("%Y-%m-%d"),
            "company_id": 1,
            "source": "manual",
            "lang": "ca_ES",
            "gender": "male",
            "birthdate": "1960-11-03",
            "iban": "ES6020808687312159493841",
            "vat": "49013933J",
            "nationality": "ES",
            "payment_type": "single",
            "discovery_channel_id": 1,
        }

    def test_route_create_new_cooperator(self):
        cooperator_vals = self.vals_subscription.copy()
        cooperator_vals["type"] = "new"

        url = "/api/subscription-request"
        response = self.http_post(url, data=cooperator_vals)
        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content.decode("utf-8"))

        self.assertIn("id", content)
        sr = self.env["subscription.request"].search(
            [
                ("_api_external_id", "=", content["id"]),
                ("name", "=", cooperator_vals["name"]),
            ]
        )

        self.assertEquals(sr.iban, cooperator_vals["iban"])
        self.assertEquals(
            sr.vat, VATNormalizer(cooperator_vals["vat"]).convert_spanish_vat()
        )
        self.assertEquals(sr.type, "new")
        self.assertEquals(sr.payment_type, cooperator_vals["payment_type"])
        self.assertEquals(sr.state_id.code, cooperator_vals["address"]["state"])
        self.assertEquals(
            sr.share_product_id.id,
            self.browse_ref(
                "somconnexio.cooperator_share_product"
            ).product_variant_id.id,
        )
        self.assertEquals(sr.ordered_parts, 1)
        self.assertEquals(sr.gender, "male")
        self.assertEquals(sr.birthdate, date(1960, 11, 3))
        self.assertEquals(sr.firstname, cooperator_vals["firstname"])
        self.assertEquals(sr.lastname, cooperator_vals["lastname"])
        sr.validate_subscription_request()
        partner_id = sr.partner_id
        self.assertEquals(partner_id.state_id.code, cooperator_vals["address"]["state"])
        self.assertEquals(
            partner_id.country_id.code, cooperator_vals["address"]["country"]
        )
        self.assertEquals(partner_id.vat, "ES{}".format(cooperator_vals["vat"]))
        self.assertEquals(
            partner_id.bank_ids.acc_number.replace(" ", ""), cooperator_vals["iban"]
        )
        self.assertEquals(partner_id.nationality.code, cooperator_vals["nationality"])
        self.assertEquals(sr.source, "manual")

    def test_route_create_sponsorship(self):
        sponsored_vals = self.vals_subscription.copy()
        sponsored_vals["type"] = "sponsorship"
        del sponsored_vals["source"]
        cooperator = self.env.ref("somconnexio.res_partner_1_demo")
        sponsored_vals["sponsor_vat"] = cooperator.vat
        sponsored_vals.pop("iban")

        url = "/api/subscription-request"
        response = self.http_post(url, data=sponsored_vals)
        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content.decode("utf-8"))

        sr = self.env["subscription.request"].search(
            [
                ("_api_external_id", "=", content["id"]),
                ("name", "=", sponsored_vals["name"]),
            ]
        )

        self.assertEquals(sr.sponsor_id.id, cooperator.id)
        self.assertFalse(sr.coop_agreement_id)
        self.assertEquals(sr.type, "sponsorship")
        self.assertEquals(sr.ordered_parts, 0)
        self.assertEquals(sr.source, "website")

    def test_route_create_sponsorship_coop_agreement(self):
        coop_agreement_vals = self.vals_subscription.copy()
        coop_agreement = self.env.ref("somconnexio.coop_agreement_1_demo")
        coop_agreement_vals.update(
            {
                "type": "sponsorship_coop_agreement",
                "coop_agreement": coop_agreement.code,
            }
        )
        coop_agreement_vals["source"] = "website_change_owner"
        url = "/api/subscription-request"
        response = self.http_post(url, data=coop_agreement_vals)
        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content.decode("utf-8"))

        sr = self.env["subscription.request"].search(
            [
                ("_api_external_id", "=", content["id"]),
                ("name", "=", coop_agreement_vals["name"]),
            ]
        )

        self.assertEquals(sr.coop_agreement_id, coop_agreement)
        self.assertEquals(sr.type, "sponsorship_coop_agreement")
        self.assertFalse(sr.sponsor_id)
        self.assertEquals(sr.ordered_parts, 0)
        self.assertEquals(sr.source, "website_change_owner")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_create_sponsorship_coop_agreement_bad_code(self):
        coop_agreement_vals = self.vals_subscription.copy()
        coop_agreement_vals.update(
            {"type": "sponsorship_coop_agreement", "coop_agreement": "fake-code"}
        )

        url = "/api/subscription-request"
        response = self.http_post(url, data=coop_agreement_vals)
        self.assertEquals(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "Coop Agreement code fake-code not found")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_create_bad_voluntary_contribution(self):
        cooperator_vals = self.vals_subscription.copy()
        cooperator_vals["type"] = "new"
        cooperator_vals["voluntary_contribution"] = "XXX"

        url = "/api/subscription-request"
        response = self.http_post(url, data=cooperator_vals)
        self.assertEquals(response.status_code, 400)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_create_bad_payment_type(self):
        cooperator_vals = self.vals_subscription.copy()
        cooperator_vals["type"] = "new"
        cooperator_vals["payment_type"] = "XXX"

        url = "/api/subscription-request"
        response = self.http_post(url, data=cooperator_vals)
        self.assertEquals(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "Payment type XXX not valid")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_create_bad_nationality(self):
        cooperator_vals = self.vals_subscription.copy()
        cooperator_vals["type"] = "new"
        cooperator_vals["nationality"] = "XXX"

        url = "/api/subscription-request"
        response = self.http_post(url, data=cooperator_vals)
        self.assertEquals(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "Nationality XXX not found")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_create_bad_state(self):
        cooperator_vals = self.vals_subscription.copy()
        cooperator_vals["type"] = "new"
        self.vals_subscription["address"]["state"] = "XXX"

        url = "/api/subscription-request"
        response = self.http_post(url, data=cooperator_vals)
        self.assertEquals(response.status_code, 400)

        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "State XXX not found")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_create_bad_source(self):
        cooperator_vals = self.vals_subscription.copy()
        cooperator_vals["type"] = "new"
        cooperator_vals["source"] = "XXX"

        url = "/api/subscription-request"
        response = self.http_post(url, data=cooperator_vals)
        self.assertEquals(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "source.+unallowed value XXX")

    def test_route_create_new_company_cooperator(self):
        cooperator_vals = self.vals_subscription.copy()
        cooperator_vals["type"] = "new"
        cooperator_vals["is_company"] = True
        cooperator_vals["company_name"] = "Manuel Coop"
        del cooperator_vals["birthdate"]
        del cooperator_vals["gender"]

        url = "/api/subscription-request"
        response = self.http_post(url, data=cooperator_vals)
        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content.decode("utf-8"))

        self.assertIn("id", content)
        sr = self.env["subscription.request"].search(
            [
                ("_api_external_id", "=", content["id"]),
                ("name", "=", cooperator_vals["company_name"]),
            ]
        )

        self.assertEquals(sr.company_email, cooperator_vals["email"])
