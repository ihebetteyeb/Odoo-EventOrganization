{
    "name": "Event Organization",
    "category": '',
    "version": "0.1",
    "depends": ["base", "web"],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/base_menu.xml",
        "views/event_view.xml",
        "views/room_view.xml",
        "wizard/change_state_wizard_view.xml",
    ],
}