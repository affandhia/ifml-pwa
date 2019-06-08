# the key's value:
#   dict: as a folder
#   string: as a file, this is the path

# those key which values is emtpy string will be changed by the project_writer

default_structure = {
    "README.md": "",
    "package.json": "",
    ".env": "",
    "yarn.lock": "main/template/file/react/assets",
    "public": {
        "favicon.ico": "main/template/file/react/assets/public",
        "index.html": "",
        "manifest.json": ""
    },
    "src": {
        'services': {},
        "utils": {
            "environment.js": "main/template/file/react/assets/src/utils"
        },
        "index.js": "",
        "logo.svg": "main/template/file/react/assets/src",
        "serviceWorker.js": "main/template/file/react/assets/src",
        "setupProxy.js.example": "main/template/file/react/assets/src",
    }
}
