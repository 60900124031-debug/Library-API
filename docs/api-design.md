Aktor: member, admin.

Method	Endpoint	Akses	Fungsi
POST	/auth/register	publik	Daftar member baru (sekaligus data anggota)
POST	/auth/login	publik	Mendapat JWT
GET	/auth/me	login	Cek token
GET	/books	login	Daftar buku (q, skip, limit)
GET	/books/{id}	login	Detail buku
POST	/books	admin	Tambah buku
PATCH	/books/{id}	admin	Ubah sebagian data buku
DELETE	/books/{id}	admin	Hapus buku
POST	/members	admin	Tambah anggota
GET	/members	admin	Daftar anggota
GET	/members/{id}	admin	Detail anggota
POST	/loans	admin, member	Pinjam buku (member hanya atas nama sendiri)
POST	/loans/{id}/return	admin	Kembalikan buku, hitung denda
GET	/loans/overdue	admin	Daftar pinjaman terlambat
GET	/loans/member/{id}	admin, member	Riwayat pinjaman (member hanya miliknya)
POST	/payments	admin, member	Bayar denda (member hanya dendanya sendiri)
GET	/payments	admin, member	Riwayat pembayaran (member hanya miliknya)

Aturan bisnis yang dipegang sepanjang praktikum:

Role saat register selalu member. Jangan pernah menerima role dari body request. Akun admin dibuat lewat skrip.
ISBN buku harus unik (409).
Email dan username harus unik (409).
Meminjam mengurangi stok. Stok 0 tidak bisa dipinjam (400).
Satu anggota maksimal 3 pinjaman aktif (400).
Anggota yang punya pinjaman terlambat tidak boleh meminjam (400).
Durasi pinjam 7 hari, denda Rp1.000 per hari keterlambatan (otomatis).
Mengembalikan buku menambah stok dan menghitung denda dalam satu transaksi.
Buku yang sudah dikembalikan tidak bisa dikembalikan dua kali (409).
Denda hanya bisa dibayar setelah buku dikembalikan dan denda lebih dari 0 (400).
Jumlah pembayaran harus sama persis dengan denda (400).
Denda yang sudah dibayar tidak bisa dibayar lagi (409).
Anggota yang punya denda belum lunas tidak boleh meminjam (400).