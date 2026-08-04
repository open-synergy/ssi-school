# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
"""Shared helper deriving ``operating_unit_id`` from ``school_id``.

Plain functions (not an Odoo model), mirroring
``school_admission_operating_unit_mixin`` in
``ssi_school_admission_operating_unit``, so the ``school_enrollment``
``create``/``write`` overrides do not duplicate the derivation logic.
"""


def get_operating_unit_id_from_school(env, school_id):
    """Return the id of a school's own operating unit, if unambiguous.

    Applies the rule: a school's operating unit is only used when the
    school has exactly one. When the school has zero or more than one
    operating unit, the caller's existing value must be left as-is.

    :param env: the current Odoo environment
    :param school_id: id of the ``school`` record, or a falsy value
    :return: id of the ``operating.unit`` record when the school has
        exactly one operating unit; ``None`` otherwise
    """
    if not school_id:
        return None
    school = env["school"].browse(school_id)
    operating_units = school.operating_unit_ids
    if len(operating_units) == 1:
        return operating_units.id
    return None


def derive_operating_unit_from_school_vals(env, vals):
    """Mutate ``vals`` in place, deriving ``operating_unit_id``.

    Applies only when ``school_id`` is present in ``vals`` and the
    caller has not already supplied ``operating_unit_id`` explicitly in
    the same ``vals`` dict — an explicit value always wins. Used from
    both ``create`` (where it overrides the
    ``mixin.single_operating_unit`` user-default by populating the key
    before the ORM applies it) and ``write`` (where it only triggers
    when ``school_id`` itself changes).

    :param env: the current Odoo environment
    :param vals: the ``create``/``write`` values dict, mutated in place
    :return: None
    """
    if "school_id" not in vals or "operating_unit_id" in vals:
        return
    operating_unit_id = get_operating_unit_id_from_school(env, vals.get("school_id"))
    if operating_unit_id:
        vals["operating_unit_id"] = operating_unit_id
