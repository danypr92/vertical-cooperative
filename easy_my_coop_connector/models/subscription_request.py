# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

from .subscription_request_adapter import SubscriptionRequestAdapter


class SubscriptionRequest(models.Model):
    _inherit = "subscription.request"

    source = fields.Selection(selection_add=[("emc_api", "Easy My Coop API")])
    binding_id = fields.One2many(
        comodel_name="emc.binding.subscription.request",
        inverse_name="internal_id",
        string="Binding ID",
        required=False,
    )

    @api.model
    def fetch_subscription_requests(self, date_from=None, date_to=None):
        SRBinding = self.env["emc.binding.subscription.request"]

        backend = self.env["emc.backend"].search([("active", "=", True)])
        backend.ensure_one()

        adapter = SubscriptionRequestAdapter(backend=backend)
        requests_dict = adapter.search(date_from=date_from, date_to=date_to)
        for request_dict in requests_dict["rows"]:
            external_id = request_dict["id"]
            request_values = adapter.to_write_values(request_dict)
            sr_binding = SRBinding.search_binding(backend, external_id)
            if sr_binding:  # update request
                sr_binding.internal_id.write(request_values)
            else:
                srequest = self.env["subscription.request"].create(
                    request_values
                )
                SRBinding.create(
                    {
                        "backend_id": backend.id,
                        "external_id": external_id,
                        "internal_id": srequest.id,
                    }
                )

    @api.model
    def backend_read(self, external_id):
        SRBinding = self.env["emc.binding.subscription.request"]

        backend = self.env["emc.backend"].search([("active", "=", True)])
        backend.ensure_one()

        adapter = SubscriptionRequestAdapter(backend)
        sr_data = adapter.read(external_id)
        # todo 404

        request_values = adapter.to_write_values(sr_data)
        sr_binding = SRBinding.search_binding(backend, external_id)

        if sr_binding:  # update request
            srequest = sr_binding.internal_id.write(request_values)
        else:
            srequest = self.env["subscription.request"].create(request_values)
            SRBinding.create(
                {
                    "backend_id": backend.id,
                    "external_id": external_id,
                    "internal_id": srequest.id,
                }
            )
        return srequest