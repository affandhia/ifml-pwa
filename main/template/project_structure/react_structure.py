# the key's value:
#   dict: as a folder
#   string: as a file, this is the path
#       those key which values is emtpy string will be changed by the project_writer

from main.utils.jinja.angular import base_file_writer

default_structure = {
    "README.md": "",
    "package.json": "",
    "public": {
        "favicon.ico": "main/template/file/react/assets/public",
        "index.html": "main/template/file/react/assets/public",
        "manifest.json": "main/template/file/react/assets/public"
    },
    "src": {
        "App.js": "",
        # "components": {
        #     "Form": {
        #         "index.js": ""
        #     },
        #     "Navbar": {
        #         "index.js": ""
        #     }
        # },
        # "containers": {
        #     "AddCustomerPage": {
        #         "index.js": ""
        #     },
        #     "Authentication": {
        #         "index.js": ""
        #     },
        #     "CustomerPage": {
        #         "components": {
        #             "Navbar": {
        #                 "index.js": ""
        #             }
        #         },
        #         "index.js": ""
        #     },
        #     "DetailCustomerPage": {
        #         "index.js": ""
        #     },
        #     "ListAccountPage": {
        #         "index.js": ""
        #     },
        #     "ListCustomerPage": {
        #         "index.js": ""
        #     },
        #     "LoginPage": {
        #         "index.js": ""
        #     }
        # },
        "index.js": "",
        "logo.svg": "main/template/file/react/assets/src",
        "serviceWorker.js": "main/template/file/react/assets/src",
        "setupProxy.js.example": "main/template/file/react/assets/src",
        "utils": {
            "token.js": ""
        }
    },
    "yarn.lock": "main/template/file/react/assets"
}
