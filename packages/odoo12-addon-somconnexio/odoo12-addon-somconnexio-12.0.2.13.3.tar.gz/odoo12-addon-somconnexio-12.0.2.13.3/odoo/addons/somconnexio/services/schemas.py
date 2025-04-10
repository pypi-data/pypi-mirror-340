def boolean_validator(field, value, error):
    if value and value not in ["true", "false"]:
        error(field, "Must be a boolean value: true or false")


S_ADDRESS_CREATE = {
    "street": {"type": "string", "required": True, "empty": False},
    "street2": {"type": "string"},
    "zip_code": {"type": "string", "required": True, "empty": False},
    "city": {"type": "string", "required": True, "empty": False},
    "country": {"type": "string", "required": True, "empty": False},
    "state": {"type": "string"},
}

S_ISP_INFO_CREATE = {
    "phone_number": {"type": "string"},
    "type": {"type": "string"},
    "delivery_address": {
        "nullable": True,
        "type": "dict",
        "schema": S_ADDRESS_CREATE
    },
    "invoice_address": {
        "type": "dict",
        "schema": S_ADDRESS_CREATE
    },
    "previous_provider": {"type": "integer"},
    "previous_owner_vat_number": {"type": "string"},
    "previous_owner_name": {"type": "string"},
    "previous_owner_first_name": {"type": "string"},
}

S_MOBILE_ISP_INFO_CREATE = {
    "icc": {"type": "string"},
    "icc_donor": {"type": "string"},
    "previous_contract_type": {"type": "string"},
    "fiber_linked_to_mobile_offer": {"type": "string"},
    "shared_bond_id": {"empty": True},
}

S_BROADBAND_ISP_INFO_CREATE = {
    "service_address": {
        "type": "dict",
        "schema": S_ADDRESS_CREATE
    },
    "keep_phone_number": {"type": "boolean"},
    "previous_service": {
        "type": "string",
        "allowed": ["", "adsl", "fiber", "4G"]
    },
}

S_CRM_LEAD_RETURN_CREATE = {
    "id": {"type": "integer"}
}

S_CRM_LEAD_CREATE = {
    "iban": {"type": "string", "required": True, "empty": False},
    "phone": {"type": "string", "nullable": True},
    "tag_codes": {"type": "list", "schema": {"type": "string"}, "nullable": True},
    "is_company": {"type": "boolean"},
    "subscription_request_id": {
        "type": "integer",
        "empty": False,
        "required": True,
        'excludes': ['partner_id'],
    },
    "partner_id": {
        "type": "string",
        "empty": False,
        "required": True,
        'excludes': ['subscription_request_id'],
    },
    "lead_line_ids": {
        "type": "list",
        "empty": False,
        "schema": {
            "type": "dict",
            "schema": {
                "product_code": {"type": "string", "required": True},
                "broadband_isp_info": {
                    "type": "dict",
                    # Merging dicts in Python 3.5+
                    # https://www.python.org/dev/peps/pep-0448/
                    "schema": {**S_ISP_INFO_CREATE, **S_BROADBAND_ISP_INFO_CREATE}  # noqa
                },
                "mobile_isp_info": {
                    "type": "dict",
                    "schema": {**S_ISP_INFO_CREATE, **S_MOBILE_ISP_INFO_CREATE}  # noqa
                },
            }
        },
    }
}
S_CONTRACT_SERVICE_INFO_CREATE = {
    "phone_number": {"type": "string", "required": True, "empty": False},
}

S_CONTRACT_ROUTER_MAC_ADDRESS_CREATE = {
    "router_mac_address": {
        "type": "string", "required": False, "empty": True,
        "regex": "-|^[0-9A-F]{2}([-:]?)[0-9A-F]{2}(\\1[0-9A-F]{2}){4}$"
    },
}
S_MOBILE_CONTRACT_SERVICE_INFO_CREATE = {
    "icc": {"type": "string", "required": True, "empty": False},
    "shared_bond_id": {"empty": True},
}
S_ADSL_CONTRACT_SERVICE_INFO_CREATE = {
    "administrative_number": {"type": "string", "required": True, "empty": False},
    "router_product_id": {"type": "string", "required": True},
    "router_serial_number": {"type": "string", "required": True, "empty": False},
    "ppp_user": {"type": "string", "required": True, "empty": False},
    "ppp_password": {"type": "string", "required": True, "empty": False},
    "endpoint_user": {"type": "string", "required": True, "empty": False},
    "endpoint_password": {"type": "string", "required": True, "empty": False},
}

S_VODAFONE_ROUTER_4G_CONTRACT_SERVICE_INFO_CREATE = {
    "vodafone_id": {"type": "string", "required": True, "empty": False},
    "vodafone_offer_code": {"empty": True},
    "router_product_id": {"type": "string", "required": True},
    "icc": {"type": "string", "required": True},
}

S_VODAFONE_FIBER_CONTRACT_SERVICE_INFO_CREATE = {
    "vodafone_id": {"type": "string", "required": True, "empty": False},
    "vodafone_offer_code": {"empty": True},
}

S_MM_FIBER_CONTRACT_SERVICE_INFO_CREATE = {
    "mm_id": {"type": "string", "required": True, "empty": False},
}

S_ORANGE_FIBER_CONTRACT_SERVICE_INFO_CREATE = {
    "suma_id": {"type": "string", "required": True, "empty": False},
}

S_XOLN_FIBER_CONTRACT_SERVICE_INFO_CREATE = {
    "external_id": {"type": "string", "required": True, "empty": False},
    "id_order": {"type": "string", "required": True, "empty": False},
    "project": {"type": "string", "required": True, "empty": False},
    "router_product_id": {"type": "string", "required": True},
    "router_serial_number": {"type": "string", "required": True, "empty": False},
}

S_CONTRACT_CREATE = {
    "code": {"type": "string", "required": False, "empty": False},
    "iban": {"type": "string", "required": True, "empty": False},
    "email": {"type": "string", "required": True, "empty": True},
    "mobile_contract_service_info": {
        "type": "dict",
        "schema": {
            **S_CONTRACT_SERVICE_INFO_CREATE,
            **S_MOBILE_CONTRACT_SERVICE_INFO_CREATE
        }
    },
    "adsl_contract_service_info": {
        "type": "dict",
        "schema": {
            **S_CONTRACT_SERVICE_INFO_CREATE,
            **S_CONTRACT_ROUTER_MAC_ADDRESS_CREATE,
            **S_ADSL_CONTRACT_SERVICE_INFO_CREATE
        }
    },
    "vodafone_fiber_contract_service_info": {
        "type": "dict",
        "schema": {
            **S_CONTRACT_SERVICE_INFO_CREATE,
            **S_VODAFONE_FIBER_CONTRACT_SERVICE_INFO_CREATE
        },
    },
    "router_4G_service_contract_info": {
        "type": "dict",
        "schema": {
            **S_CONTRACT_SERVICE_INFO_CREATE,
            **S_VODAFONE_ROUTER_4G_CONTRACT_SERVICE_INFO_CREATE
        },
    },
    "mm_fiber_contract_service_info": {
        "type": "dict",
        "schema": {
            **S_CONTRACT_SERVICE_INFO_CREATE,
            **S_MM_FIBER_CONTRACT_SERVICE_INFO_CREATE,
        }
    },
    "orange_fiber_contract_service_info": {
        "type": "dict",
        "schema": {
            **S_ORANGE_FIBER_CONTRACT_SERVICE_INFO_CREATE,
        }
    },
    "xoln_fiber_contract_service_info": {
        "type": "dict",
        "schema": {
            **S_CONTRACT_SERVICE_INFO_CREATE,
            **S_CONTRACT_ROUTER_MAC_ADDRESS_CREATE,
            **S_XOLN_FIBER_CONTRACT_SERVICE_INFO_CREATE,
        }
    },
    "partner_id": {"type": "string", "required": True},
    "service_address": {"type": "dict", "schema": S_ADDRESS_CREATE},
    "service_technology": {"type": "string", "required": True, "empty": False},
    "service_supplier": {"type": "string", "required": True, "empty": False},
    "fiber_signal_type": {
        "type": "string",
        "allowed": ["", "fibraCoaxial", "fibraFTTH", "fibraIndirecta", "NEBAFTTH"]
    },
    "contract_lines": {
        "type": "list",
        "dependencies": {'contract_line': None},
        "schema": {
            "type": "dict",
            "schema": {
                "product_code": {"type": "string", "required": True},
                "date_start": {
                    "type": "string", "required": True,
                    "regex": "\\d{4}-[01]\\d-[0-3]\\d [0-2]\\d:[0-5]\\d:[0-5]\\d"
                }
            }
        }
    },
    # We must evaluate the "contract_line" field because OTRS cannot send a list
    # with only one element, so we do this differentiation to know how to treat it.
    "contract_line": {
        "type": "dict",
        "dependencies": {'contract_lines': None},
        "schema": {
            "product_code": {"type": "string", "required": True},
            "date_start": {
                "type": "string", "required": True,
                "regex": "\\d{4}-[01]\\d-[0-3]\\d [0-2]\\d:[0-5]\\d:[0-5]\\d"
            }
        }
    },
    "ticket_number": {"type": "string", "required": True},
    # OTRS sends a '{}' as empty value for parent_pack_contract_id.
    # Therefore, we can't restrict this field as string
    # if we want to avoid BadRequest errors
    "parent_pack_contract_id": {"empty": True},
    # OTRS sends a '{}' as empty value for mobile_pack_contracts.
    # Therefore, we can't restrict this field as string
    # if we want to avoid BadRequest errors
    "mobile_pack_contracts": {"empty": True},
}

S_CONTRACT_RETURN_CREATE = {
    "id": {"type": "integer"}
}

S_PREVIOUS_PROVIDER_REQUEST_SEARCH = {
    "mobile": {"type": "string", "check_with": boolean_validator},
    "broadband": {"type": "string", "check_with": boolean_validator},
}

S_PREVIOUS_PROVIDER_RETURN_SEARCH = {
    "count": {"type": "integer"},
    "providers": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "id": {"type": "integer", "required": True},
                "name": {"type": "string", "required": True},
            }
        }
    }
}

S_DISCOVERY_CHANNEL_REQUEST_SEARCH = {"_id": {"type": "integer"}}

S_DISCOVERY_CHANNEL_RETURN_SEARCH = {
    "discovery_channels": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "id": {"type": "integer", "required": True},
                "name": {"type": "string", "required": True},
            }
        }
    }
}

S_PRODUCT_CATALOG_REQUEST_SEARCH = {
    "code": {"type": "string"},
    "categ": {
        "type": "string",
        "allowed": ["mobile", "adsl", "fiber", "4G"],
        "excludes": ["product_code"]
    },
    "product_code": {
        "type": "string",
        "excludes": ["categ", "is_company"],
    },
    "is_company": {
        "type": "string",
        "excludes": ["product_code"],
        "check_with": boolean_validator,
    },
}

S_PRODUCT_CATALOG_RETURN_SEARCH = {
    "pricelists": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "code": {"type": "string", "required": True},
                "products": {
                    "type": "list",
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "code": {"type": "string", "required": True},
                            "name": {"type": "string", "required": True},
                            "price": {"type": "number", "required": True},
                            "category": {"type": "string", "required": True},
                            "minutes": {"type": "integer", "nullable": True,
                                        "required": True},
                            "data": {"type": "integer", "nullable": True,
                                     "required": True},
                            "bandwidth": {"type": "integer", "nullable": True,
                                          "required": True},
                            "has_landline_phone": {"type": "boolean"},
                            "available_for": {
                                "type": "list",
                                "required": True,
                                "schema": {
                                    "type": "string",
                                },
                            },
                            "offer": {
                                "type": "dict",
                                "schema": {
                                    "code": {"type": "string", "required": True},
                                    "price": {"type": "number", "required": True},
                                    "name": {"type": "string", "required": True},
                                },
                                "required": False
                            }
                        }
                    }
                },
                "packs": {
                    "type": "list",
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "code": {"type": "string", "required": True},
                            "name": {"type": "string", "required": True},
                            "price": {"type": "number", "required": True},
                            "category": {"type": "string", "required": True},
                            "available_for": {
                                "type": "list",
                                "required": True,
                                "schema": {
                                    "type": "string",
                                },
                            },
                            "mobiles_in_pack": {"type": "number", "required": True},
                            "fiber_bandwidth": {"type": "number", "required": True},
                            "has_land_line": {"type": "boolean", "required": True},
                            "products": {
                                "type": "list",
                                "schema": {
                                    "type": "dict",
                                    "schema": {
                                        "code": {"type": "string", "required": True},
                                        "name": {"type": "string", "required": True},
                                        "price": {"type": "number", "required": True},
                                        "category": {
                                            "type": "string", "required": True
                                        },
                                        "minutes": {"type": "integer", "nullable": True,
                                                    "required": True},
                                        "data": {"type": "integer", "nullable": True,
                                                 "required": True},
                                        "bandwidth": {
                                            "type": "integer", "nullable": True,
                                            "required": True},
                                        "has_landline_phone": {"type": "boolean"},
                                    },
                                }
                            }
                        }
                    }
                }
            },
        }
    }
}

S_ONE_SHOT_CATALOG_REQUEST_SEARCH = {
    "code": {"type": "string"},
    "product_code": {"type": "string"},
}


S_ONE_SHOT_CATALOG_RETURN_SEARCH = {
    "pricelists": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "code": {"type": "string", "required": True},
                "one_shots": {
                    "type": "list",
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "code": {"type": "string", "required": True},
                            "name": {"type": "string", "required": True},
                            "price": {"type": "number", "required": True},
                            "minutes": {
                                "type": "integer",
                                "nullable": True,
                                "required": True,
                            },
                            "data": {
                                "type": "integer",
                                "nullable": True,
                                "required": True,
                            },
                        },
                    },
                },
            },
        },
    }
}

S_CONTRACT_ONE_SHOT_ADDITION = {
    "product_code": {"type": "string", "required": True},
    "phone_number": {"type": "string", "required": True},
}

S_CONTRACT_CHANGE_TARIFF = {
    "product_code": {"type": "string", "required": True},
    "phone_number": {"type": "string", "empty": True},
    "code": {"type": "string", "empty": True},
    "start_date": {"empty": True},
    # OTRS sends a '{}' as empty value for parent_pack_contract_id.
    # Therefore, we can't restrict this field as string
    # if we want to avoid BadRequest errors
    "parent_pack_contract_id": {"empty": True},
    "shared_bond_id": {"empty": True}
}

S_RES_PARTNER_REQUEST_GET = {"_id": {"type": "integer"}}

S_RES_PARTNER_REQUEST_SEARCH = {
    "vat": {"type": "string", "required": True},
}

S_RES_PARTNER_RETURN_GET = {
    "id": {"type": "integer"},
    "name": {"type": "string"},
    "firstname": {"type": "string"},
    "lastname": {"type": "string"},
    "display_name": {"type": "string"},
    "ref": {"type": "string"},
    "lang": {"type": "string"},
    "vat": {"type": "string"},
    "type": {"type": "string"},
    "email": {"type": "string"},
    "phone": {"type": "string"},
    "mobile": {"type": "string"},
    "birthdate_date": {"type": "string"},
    "cooperator_register_number": {"type": "integer"},
    "cooperator_end_date": {"type": "string"},
    "coop_agreement_code": {"type": "string"},
    "sponsorship_code": {"type": "string"},
    "sponsor_ref": {"type": "string"},
    "sponsees_number": {"type": "integer"},
    "sponsees_max": {"type": "integer"},
    "coop_candidate": {"type": "boolean"},
    "member": {"type": "boolean"},
    "addresses": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": S_ADDRESS_CREATE
        }
    },
    "banned_actions": {
        "type": "list",
        "schema": {"type": "string"}
    },
    "inactive_sponsored": {"type": "boolean"},
    "is_company": {"type": "boolean"},
}

S_ACCOUNT_INVOICE_CREATE = {
    "groupCode": {"type": "string", "required": True, "regex": "^[0-9]+(_[0-9]*)+"},
    "id_billing_run": {"type": "string", "required": True},
    "invoiceDate": {
        "type": "integer",
        "required": True,
    },
    "invoiceLines": {
        "type": "list",
        "required": True,
        "empty": False,
        "schema": {
            "type": "dict",
            "schema": {
                "description": {"type": "string", "required": True},
                "accountingCode": {"type": "string", "required": True},
                "amountWithoutTax": {"type": "float", "required": True},
                "amountWithTax": {"type": "float", "required": True},
                "amountTax": {"type": "float", "required": True},
                "taxCode": {"type": "string", "required": True},
                "productCode": {"type": "string", "required": True},
            },
        },
    },
    "odoo_contracts": {"type": "string"},
}

S_ACCOUNT_INVOICE_UPDATE = {
    "invoice_number": {"type": "string", "required": True},
    "pdf_link": {"type": "string", "required": True},
}

S_SUBSCRIPTION_REQUEST_CREATE_SC_FIELDS = {
    "iban": {"type": "string"},
    "vat": {"type": "string", "required": True},
    "coop_agreement": {"type": "string"},
    "sponsor_vat": {"type": "string"},
    "voluntary_contribution": {"type": "float"},
    "nationality": {"type": "string"},
    "payment_type": {"type": "string", "required": True},
    "address": {"type": "dict", "schema": S_ADDRESS_CREATE},
    "type": {"type": "string", "required": True},
    "share_product": {"type": "integer", "required": False},
    "ordered_parts": {"type": "integer", "required": False},
    "discovery_channel_id": {"type": "integer", "required": True},
    "birthdate": {
        "type": "string",
        "regex": "\\d{4}-[01]\\d-[0-3]\\d"
    },
    "gender": {"type": "string"},
    "phone": {"type": "string"},
    "is_company": {"type": "boolean"},
    "company_name": {"type": "string"},
    "firstname": {"type": "string"},
    "lastname": {"type": "string"},
    "source": {
        "type": "string",
        "allowed": ["website", "crm", "manual", "operation", "website_change_owner"],
    },
}

S_SUBSCRIPTION_REQUEST_RETURN_CREATE_SC_FIELDS = {
    "share_product": {"required": False},
    "ordered_parts": {"type": "integer", "required": False},
}

S_CONTRACT_IBAN_CHANGE_CREATE = {
    "partner_id": {"type": "string", "required": True},
    "iban": {"type": "string", "required": True},
    "contracts": {"type": "string", "required": False},
    "ticket_id": {"type": "string", "required": False},
}

S_PARTNER_EMAIL_CHANGE_CREATE = {
    "partner_id": {"type": "string", "required": True},
    "email": {"type": "string", "required": True},
    "start_date": {"type": "string"},
    "summary": {"type": "string"},
    "done": {"type": "boolean"},
}

S_CONTRACT_EMAIL_CHANGE_CREATE = {
    "partner_id": {"type": "string", "required": True},
    "email": {"type": "string", "required": True},
    "contracts": {"type": ["dict", "string"], "required": True},
    "start_date": {"type": "string"},
    "summary": {"type": "string"},
    "done": {"type": "boolean"},
}

S_CONTRACT_PAGING = {
    "limit": {
        "type": "string",
    },
    "offset": {
        "type": "string",
    },
    "sortBy": {
        "type": "string",
    },
    "sortOrder": {
        "type": "string",
        "dependencies": ['sortBy']
    }
}

S_CUSTOMER_CONTRACT_MULTI_FILTER_SEARCH = {
    "customer_ref": {
        "type": "string",
        "required": True
    },
    "phone_number": {
        "type": "string",
        "dependencies": "customer_ref",
    },
    "subscription_type": {
        "type": "string",
        "dependencies": "customer_ref",
        "allowed": ["mobile", "broadband"]
    },
    **S_CONTRACT_PAGING,
}

S_CONTRACT_SEARCH = {
    "customer_ref": {
        "type": "string",
        "excludes": ["code", "partner_vat", "phone_number"],
        "required": True
    },
    "code": {
        "type": "string",
        "excludes": ["partner_vat", "phone_number", "customer_ref"],
        "required": True
    },
    "partner_vat": {
        "type": "string",
        "excludes": ["code", "phone_number", "customer_ref"],
        "required": True
    },
    "phone_number": {
        "type": "string",
        "excludes": ["partner_vat", "code", "customer_ref"],
        "required": True
    },
    **S_CONTRACT_PAGING,
}

S_CONTRACT_GET_FIBER_CONTRACTS_TO_PACK = {
    "partner_ref": {
        "type": "string",
        "required": True,
    },
    "mobiles_sharing_data": {
        "type": "string",
        "excludes": ["all"],
        "check_with": boolean_validator,
    },
    "all": {
        "type": "string",
        "excludes": ["mobiles_sharing_data"],
        "check_with": boolean_validator,
    },
}

S_SEARCH_COOP_AGREEMENT = {
    "code": {
        "type": "string",
        "required": True,
    }
}

S_RETURN_SEARCH_COOP_AGREEMENT = {
    "name": {
        "type": "string",
        "required": True,
    },
    "code": {
        "type": "string",
        "required": True,
    },
    "first_month_promotion": {
        "type": "boolean",
        "required": True,
    }
}

S_TERMINATE_CONTRACT = {
    "code": {
        "type": "string",
        "required": True,
        "empty": False,
    },
    "terminate_date": {
        "type": "string",
        "required": True,
        "empty": False,
    },
    "terminate_reason": {
        "type": "string",
        "required": True,
        "empty": False,
    },
    "terminate_user_reason": {
        "type": "string",
        "required": False,
    },
    "terminate_comment": {
        "type": "string",
        "required": False,
    },
}
