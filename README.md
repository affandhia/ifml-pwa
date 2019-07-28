# IFML to React Interpreter

> USER MANUAL v0.1.0

## INFORMASI UMUM

Bagian ini menjelaskan informasi dan tujuan dari sistem yang telah dibuat.

### _System Overview_

IFML to React Interpreter adalah program untuk mengubah model aplikasi web yang telah disusun dalam IFML menjadi aplikasi web berbasis React. Aplikasi web dijalankan pada suatu _server_ untuk dapat diakses oleh pengguna. Pengguna dapat mengaksesnya dengan menggunakan _browser_ pada komputer.

### Ringkasan Manual

User Manual terdiri dari empat bagian: Informasi Umum, Informasi Sistem, Persiapan, dan Penggunaan Program.

- Bagian **Informasi Umum** menjelaskan _hardware_ dan _software_ pendukung yang diperlukan untuk menjalankan programm, akses yang tersedia untuk pengguna.

- Bagian **Informasi Sistem** menjelaskan _hardware_ dan _software_ pendukung yang diperlukan untuk menjalankan programm, akses yang tersedia untuk pengguna.

- Bagian **Persiapan** menunjukan tahapan bagaimana program diperoleh dan dipersiapkan untuk dapat digunakan. Tahapan tersebut mencakup instalasi program dan instalasi _software_ pendukung pada _environment_.

- Bagian **Penggunaan Program** menunjukan cara menjalankan _interpreter_ dan hasil berupa aplikasi web.

## INFORMASI SISTEM

Bagian ini menjelaskan _hardware_ dan _software_ pendukung yang diperlukan untuk menjalankan programm, akses yang tersedia untuk pengguna.

### Konfigurasi Sistem

IFML to React Interpreter berjalan pada _platform_ yang telah terpasang **Python** versi **3.6.4** atau lebih baru. _Platform_ tidak terbatas pada sistem operasi berbasis Unix selama **Python** tersedia pada sistem operasi tersebut.

Program ini tidak memerlukan internet untuk menjalankan tugas. Internet dibutuhkan ketika sistem operasi tidak tersedia **Python** dengan versi minimal yang dibutuhkan. Untuk mendapatkan **Python** yang sesuai, pengguna dapat mengakses [halaman unduh Python](https://www.python.org/downloads/) dan memilih _binary_ **Python** yang sesuai dengan sistem operasi yang digunakan.

## PERSIAPAN

Bagian ini menunjukan tahapan bagaimana program diperoleh dan dipersiapkan untuk dapat digunakan. Tahapan tersebut mencakup instalasi program dan instalasi _software_ pendukung pada _environment_.

### Instalasi

Berkas program dapat diperoleh pada _repository_ utama [affandhia/ifml-pwa](https://github.com/affandhia/ifml-pwa). Terdapat dua metode untuk memperoleh berkas program.

#### Metode 1: Mengunduh Berkas `.zip`

Berkas dapat diperoleh dengan mengakses [tautan ini](https://github.com/affandhia/ifml-pwa/archive/release.zip). Berkas berupa _file_ berekstensi `.zip` yang harus diekstrak. Pada berkas tersebut terdapat satu _folder_ bernama `ifml-pwa-release` yang mengadung program.

> Bila tautan tidak dapat diakses, berkas dapat diperoleh dengan membuka
> halaman utama _repository_ utama
> [affandhia/ifml-pwa](https://github.com/affandhia/ifml-pwa). Pada
> halaman utama tekan tombol **"Clone or download"** lalu tekan tombol
> **"Download ZIP"**.

#### Metode 2: _Clone Repository_ Menggunakan **Git**

Berkas dapat juga diperoleh dengan menggunakan program bernama **Git** versi **2.20.1** atau lebih. Proses tersebut dinamakan _clone_. Untuk melakukan _clone_, sistem harus menjalankan perintah:

```
git clone https://github.com/affandhia/ifml-pwa
```

Folder `ifml-pwa` akan tersedia ketika **Git** telah selesai melakukan _clone_ terhadap _repository_.

#### Konten dari Folder Program

Program terdiri dari beberapa _folder_ dan _file_. Secara umum, keseluruhan berkas akan terlihat seperti susunan dibawah ini:

```
—folder utama—
├── MANIFEST.in
├── abs_bankaccount.core
├── abs_bankaccount.uml
├── custom_xmi_parser
│   └── ...
├── ifml_parser
│   └── ...
├── ifml_to_react.py
├── main
│   └── ...
├── requirements.txt
├── setup.cfg
├── setup.py
└── test
    └── ...
```

> Tanda `...` merupakan _placeholder_ dari isi _folder_ diatasnya.

### Instalasi _Software_ Pendukung dan _Environment_

#### _Software_ Pendukung

Untuk menjalankan aplikasi web, sistem operasi harus sudah terpasang **NodeJS**. **NodeJS** yang diperlukan adalah **NodeJS** versi **10.9.0** atau lebih baru. **NodeJS** dikategorikan ke dalam _software_ pendukung karena tidak dibutuhkan pada proses utama dari program ini. **NodeJS** dapat diperoleh dengan menjalankan _binary_ yang tersedia pada [halaman unduh NodeJS](https://nodejs.org/en/download/).

#### _Environment_ **Python**

Pada folder utama dari program telah tersedia berkas bernama `requirements.txt`. Berkas ini mengandung daftar _software_ pendukung yang diperlukan untuk menjalankan program. _Software_ pendukung tersebut dibuat dalam bahasa **Python** yang dapat dipasang langsung.

1.  **Package Manager** khusus **Python** bernama **pip** harus sudah terpasang pada sistem operasi. **pip** dapat diperoleh dengan mengikuti proses instalasi pada [halaman ini](https://pip.pypa.io/en/stable/installing/).
2.  Pastikan **terminal** atau **command prompt** pada sistem operasi telah menunjuk ke folderr utama program yang mengandung berkas `requirements.txt`.
3.  Jalankan perintah `pip install -r requirements.txt` dan tunggu hingga proses selesai.
4.  _Software_ pendukung dan _environment_ sudah siap bila perintah sukses dijalankan tanpa ada eror.

## PENGGUNAAN PROGRAM

Bagian ini menunjukan cara menjalankan _interpreter_ dan hasil berupa aplikasi web.

### Pengunaan _IFML to React Interpreter_

Untuk menjalankan program, berkas IFML berekstesi `.core` dan UML berekstensi `.uml` dibutuhkan oleh _interpreter_. Berkas tersebut harus diletakan pada _folder_ yang sama dengan program. Program tersebut berupa berkas `ifml_to_react.py`. Langkah untuk menjalankan _interpreter_ adalah:

1.  Pastikan **terminal** atau **command prompt** pada sistem operasi telah menunjuk ke _folder_ utama program yang mengandung berkas `ifml_to_react.py`, `<nama aplikasi>.core`, dan `<nama aplikasi>.uml`.
2.  Jalankan perintah `python ifml_to_react.py` dan tunggu hingga proses selesai hingga menunjukan pesan `INFO React PWA Project successfully generated at result`.
3.  _Folder_ **result/`\<nama aplikasi>`** akan terbuat secara otomatis.
4.  Hasil dari _interpreter_ terdapat dalam _folder_ `<nama aplikasi>`.

```
├── ...
├── result
│   └── <nama aplikasi>
├── ...
```

#### Konfigurasi

Ketika pertama kali memasang program, program telah siap untuk dijalankan dengan konfigurasi dasar. Konfigurasi tersebut mempengaruhi hasil dari aplikasi web yang akan digunakan.

##### Nama Aplikasi

`<nama aplikasi>` pada tahap sebelumnya merupakan _placeholder_ untuk nama berkas yang diperlukan. Ketika pertama kali memasang program, berkas awal `<nama aplikasi>` yang tersedia adalah `abs_bankaccount`. Pada folder utama dapat ditemukan berkas `abs_bankaccount.core` dan `abs_bankaccount.uml`.

Untuk mengganti nama aplikasi, `abs_bankaccount` diganti menjadi nama yang diinginkan. Hal yang perlu diganti adalah:

- Berkas `abs_bankaccount.core`
- Berkas `abs_bankaccount.uml`
- Sesuaikan variabel `ifml_file` dan `uml_file` pada _line_ 15 dan 17 dalam berkas `ifml_to_react.py` dengan nama berkas yang telah diganti.

##### Google Client ID

Ini digunakan oleh aplikasi web untuk proses autentikasi. Proses autentikasi ini membutuhkan internet dan juga _server_ API **ABS Microservice** yang tersedia atau yang dapat dipasang secara local dengan mengakses [affandhia/abs-backend-docker](https://github.com/affandhia/abs-backend-docker). **Google Client ID** harus sama baik pada API _server_ maupun pada _interpreter_. Untuk mengubahnya dapat dengan mengganti nilai variabel `client_id` pada _line_ 13 dalam berkas `ifml_to_react.py`.

### Pengunaan Aplikasi Web dari Hasil _Interpreter_

Hasil dari interpreter berupa aplikasi web berbasis React 16 yang didukung oleh NodeJS. Prroses untuk menjalankan aplikasi web dapat mengikuti tahap berikut:

1.  Pastikan **NodeJS** versi **10.9.0** atau lebih baru dan _browser_ yang mendukung **JavaScript** versi **ES5** atau lebih baru (contoh [**Google Chrome**](https://www.google.com/chrome/) atau [**Mozilla Firefox**](https://www.mozilla.org/en-US/firefox/) terbaru).
2.  Pastikan API **ABS Microservice** ([affandhia/abs-backend-docker](https://github.com/affandhia/abs-backend-docker)) telah berjalan pada `localhost:7776`.
3.  Pastikan **terminal** atau **command prompt** pada sistem operasi telah menunjuk ke folder **result/`<nama aplikasi>`**.
4.  Jalankan perintah `npm install && npm run start:production:clean`.
5.  _Browser_ standar akan terbuka secara otomatis dan mengarahkan ke halaman [http://localhost:3001/](http://localhost:3001/).

#### Konfigurasi

Ketika pertama kali memasang program, program telah siap untuk dijalankan dengan konfigurasi dasar. Konfigurasi tersebut mempengaruhi jalannya hasil aplikasi web.

##### _Port_ yang Digunakan Aplikasi Web

_Port_ standar yang digunakan adalah 3001. Untuk mengubahnya dapat dengan mengganti _port_ angka 3001 pada _line_ 20 dalam berkas `result/<nama aplikasi>/package.json` menjadi _port_ lain yang tersedia.

##### API **ABS Microservice**

Program akan secara standar mengatur aplikasi web untuk meminta data kepada _server_ API **ABS Microservice** yang tersedia pada `localhost:7776`. Untuk mengubahnya dapat dengan mengganti `http://localhost:7776` pada _line_ 20 dalam berkas `result/<nama aplikasi>/package.json` menjadi alamat lain yang menyediakan API.
