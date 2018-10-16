from main.utils.jinja.angular import base_file_writer

default_structure = {
    'e2e': {
        'src': {
            'app.e2e-spec.ts': '',
            'app.po.ts': ''
        },
        'protractor.conf.js': '',
        'tsconfig.e2e.json': ''
    },
    'src': {
        'app': {
            'services': {},
            'app-routing.module.ts': '',
            'app.component.css': '',
            'app.component.html': '',
            'app.component.spec.ts': '',
            'app.component.ts': '',
            'app.module.ts': ''
        },
        'assets': {
            'icons': {
                'icon-72x72.png': 'main/template/file/angular/assets',
                'icon-96x96.png': 'main/template/file/angular/assets',
                'icon-128x128.png': 'main/template/file/angular/assets',
                'icon-144x144.png': 'main/template/file/angular/assets',
                'icon-152x152.png': 'main/template/file/angular/assets',
                'icon-192x192.png': 'main/template/file/angular/assets',
                'icon-384x384.png': 'main/template/file/angular/assets',
                'icon-512x512.png': 'main/template/file/angular/assets'
            },
        },
        'environments': {
            'environment.prod.ts': '',
            'environment.ts': ''
        },
        'favicon.ico': 'main/template/file/angular/assets',
        'index.html': '',
        'karma.conf.js': '',
        'main.ts': '',
        'manifest.json': '',
        'polyfills.ts': '',
        'styles.css': '',
        'test.ts': '',
        'tsconfig.app.json': '',
        'tsconfig.spec.json': '',
        'tslint.json': '',
    },
    '.editorconfig': '',
    '.gitignore': '',
    'angular.json': '',
    'ngsw-config.json': '',
    'package.json': '',
    'README.md': '',
    'server.js': '',
    'tsconfig.json': '',
    'tslint.json': ''
}