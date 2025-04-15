# Copyright 2020 ForgeFlow, S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Web Widget mpld3 Chart",
    "category": "Hidden",
    "summary": "This widget allows to display charts using MPLD3 library.",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "version": "18.0.1.0.0",
    "website": "https://github.com/OCA/web",
    "depends": ["web"],
    "data": [],
    "external_dependencies": {"python": ["mpld3==0.5.10", "beautifulsoup4"]},
    "auto_install": False,
    "development_status": "Beta",
    "maintainers": ["JordiBForgeFlow", "ThiagoMForgeFlow"],
    "license": "LGPL-3",
    "assets": {
        "web.assets_backend": [
            "web_widget_mpld3_chart/static/src/js/*.js",
            "web_widget_mpld3_chart/static/src/xml/*.xml",
        ],
    },
}
