import logging
from datetime import date

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons.queue_job.job import job

from ...services.change_partner_emails import ChangePartnerEmails
from ...somoffice.errors import SomOfficeUserChangeEmailError
from ...services.partner_email_change_process import PartnerEmailChangeProcess
from ...services.contract_email_change_process import ContractEmailChangeProcess

_logger = logging.getLogger(__name__)

boolean_selections = [
    ("yes", _("Yes")),
    ("no", "No"),
]


class PartnerEmailChangeWizard(models.TransientModel):
    _name = "partner.email.change.wizard"
    partner_id = fields.Many2one("res.partner")
    available_email_ids = fields.Many2many(
        "res.partner", string="Available Emails", compute="_compute_available_email_ids"
    )
    available_email_ids_for_partner = fields.Many2many(
        "res.partner",
        string="Available Emails for partner",
        compute="_compute_available_email_ids_for_partner",
    )

    # Change Contact Email fields
    change_contact_email = fields.Selection(
        string="Contact and OV", selection=boolean_selections, required=True
    )
    email_id = fields.Many2one(
        "res.partner",
        string="Email",
    )

    # Change Contracts Emails fields
    change_contracts_emails = fields.Selection(
        string="Contracts", selection=boolean_selections, required=True
    )
    contract_ids = fields.Many2many("contract.contract", string="Contracts")
    email_ids = fields.Many2many(
        "res.partner",
        string="Emails",
    )
    available_contract_group_ids = fields.One2many(
        "contract.group",
        string="Available Contract Groups",
        compute="_compute_available_contract_group_ids",
    )
    contract_group_id = fields.Many2one(
        "contract.group",
        string="Contract Group",
        help="The contract groups that are available for the selected contracts. "
        "Keep empty to create a new contract group.",
    )
    summary = fields.Char(translate=True, default="Email change")
    done = fields.Boolean(default=True)

    @api.multi
    @api.depends("partner_id")
    def _compute_available_email_ids(self):
        if self.partner_id:
            self.available_email_ids = [
                (6, 0, self.partner_id.get_available_emails().ids)
            ]

    @api.multi
    @api.depends("partner_id")
    def _compute_available_email_ids_for_partner(self):
        if self.partner_id:
            av_emails = self.partner_id.get_available_emails()
            email_ids = [e.id for e in av_emails if e.email != self.partner_id.email]
            self.available_email_ids_for_partner = [(6, 0, email_ids)]

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults["partner_id"] = self.env.context["active_id"]
        return defaults

    @api.multi
    def button_change(self):
        self.ensure_one()
        self.change_partner_emails = ChangePartnerEmails(self.env, self.partner_id)
        if self.change_contracts_emails == "yes":
            self._change_contract_emails()
        if self.change_contact_email == "yes":
            self._change_contact_email()
            self._change_somoffice_email()

    def _change_contact_email(self):
        self.change_partner_emails.change_contact_email(self.email_id)
        return True

    def _change_contract_emails(self):
        emails = self.email_ids or self.email_id
        activity_args = {
            "res_model_id": self.env.ref("contract.model_contract_contract").id,
            "user_id": self.env.user.id,
            "activity_type_id": self.env.ref(
                "somconnexio.mail_activity_type_contract_data_change"
            ).id,
            "date_done": date.today(),
            "date_deadline": date.today(),
            "summary": self.summary,
            "done": self.done,
        }
        self.change_partner_emails.change_contracts_emails(
            self.contract_ids,
            emails,
            activity_args,
            contract_group_id=self.contract_group_id,
            create_contract_group=not bool(self.contract_group_id),
        )
        return True

    def _change_somoffice_email(self):
        try:
            self.change_partner_emails.change_somoffice_email(self.email_id)
        except SomOfficeUserChangeEmailError as error:
            _logger.error(error)
            msg = _(
                "Couldn't change SomOffice user email. "
                + "Please contact IT department"
            )
            raise UserError(msg)
        return True

    def _get_first_day_of_next_month(self, request_date):
        if request_date.month == 12:
            return date(request_date.year + 1, 1, 1)
        else:
            return date(request_date.year, request_date.month + 1, 1)

    @job
    def run_from_api_partner(self, **params):
        service = PartnerEmailChangeProcess(self.env)
        service.run_from_api(**params)

    @job
    def run_from_api_contract(self, **params):
        service = ContractEmailChangeProcess(self.env)
        service.run_from_api(**params)

    @api.onchange("email_ids", "contract_ids")
    def _compute_available_contract_group_ids(self):
        if not self.contract_ids or not self.email_ids:
            self.available_contract_group_ids = []
            return

        self.available_contract_group_ids = (
            self.env["contract.group"]
            .search([("partner_id", "=", self.contract_ids[0].partner_id.id)])
            .filtered(
                lambda x: x.validate_contract_to_group(
                    self.contract_ids[0], email_ids=self.email_ids
                )[0]
            )
        )
        self.contract_group_id = (
            self.available_contract_group_ids[0]
            if self.available_contract_group_ids
            else False
        )
