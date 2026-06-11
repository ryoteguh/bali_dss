<h1><bold>Laporan SIstem Pendukung Keputusan (Decision Support System/DSS) di Pariwisata Bali</bold></h1>
<h4>Nama|NIM|akun GitHub</h4>
<ol>
  <li>Rio Teguh Priyo Utomo |2501010063| ryoteguh</li>
  <li>Ngakan Gede Marvyn Cakra Ajidharma |2501010078| marpinleclerc-jpg</li>
  <li>Andi Pratama |2501010092| eyka0209akssjjs0209</li>
</ol>
<br>
<div align="justify">
<h2><bold>BAB I PENDAHULUAN</bold></h2>
<h4>1.1 Latar Belakang</h4>
<p>Pulau Bali adalah salah satu destinasi populer yang ada di Indonesia. Setiap tahunnya ada jutaan wisatawan dari luar maupun dalam negeri yang berkunjung untuk mencari destinasi wisata yang berbeda-beda seperti wisata budaya, pantai maupun kuliner. Namun,melimpahnya opsi destinasi ini sering kali menimbulkan fenomena <italic>information overload</italic> bagi wisatawan. Mereka kerap mengalami kesulitan dalam merencanakan rute perjalanan yang efektif, efisien, dan sesuai dengan kondisi personal mereka. Wisatawan cenderung memilih destinasi secara acak tanpa mempertimbangkan jarak geografis yang optimal, biaya, dan faktor cuaca yang menyebabkan pemborosan waktu akibat jalur yang tidak efisien, boros biaya, dan ketidaknyamanan dalam berwisata. Oleh karena itu dibutuhkan sebuah sistem modern yang dapat membantu para wisatawan membuat keputusan lebih baik.</p>
<p>Di sistem ini struktur data graph dapat digunakan untuk mengatasi pemilihan jalur transportasi dengan menggambarkan destinasi wisata dan titik keberangkatan sebagai titik <italic>node</italic> dan jalur yang menghubungkan setiap titik sebagai <italic>edge</italic>. Lalu hubungan antar destinasi diberi bobot seperti jarak biaya dan waktu agar pemilihan jalur lebih akurat. Penggunaan algoritma <italic>Djikstra</italic> akan membantu pemilihan jalur karena mampu mengevaluasi bobot untuk mencari jalur terpendek. Selain itu algoritma <italic>Breadth-First Search (BFS) </italic> juga digunakan untuk mengetahui jangkauan wilayah wisata lalu memanfaatkan metrik <italic>Degree Centrality</italic> menentukan titik destinasi (hub) yang strategis. Namun hasil dari keputusan algoritma biasanya kaku dan sulit dipahami oleh orang awam. Maka dari itu sistem ini akan diimplementasikan dalam bentuk web dengan kecerdasan buatan Gemini AI dan pemantauan cuaca real-time menggunakan OpenWeatherMap API. </p>
<p>Berdasarkan diskusi tersebut, maka ditetapkan projek ini adalah projek membuat <strong>Sistem Pendukung Keputusan (Decision Support System/DSS) Pariwisata Bali berbasis graf</strong>. Sistem ini diharapkan dapat membantu wisatawan menyusun perencanaan wisata lebih baik,mengurangi resiko pemborosan sumber daya waktu dan biaya, serta mengimplementasikan konsep struktur data graph pada kasus di dunia nyata.</p>
<h4>1.2 Rumusan Masalah</h4>
<ol>
  <li>Bagaimana memodelkan jaringan destinasi wisata dan infrastruktur transportasi di Pulau Bali ke dalam representasi struktur data Graph menggunakan pendekatan Adjacency List?</li>
  <li>Bagaimana merancang dan mengintegrasikan model matematis graf tersebut ke dalam sebuah Decision Support System (DSS) interaktif yang dilengkapi dengan Generative AI dan data cuaca real-time untuk menghasilkan rekomendasi perjalanan yang tepat?</li>
  <li>Bagaimana mengimplementasikan algoritma Dijkstra untuk menentukan rute perjalanan yang paling optimal berdasarkan jarak, waktu, dan biaya?</li>
  <li>Bagaimana menerapkan algoritma Breadth-First Search (BFS) untuk memetakan urutan eksplorasi wilayah serta metrik Degree Centrality untuk mengidentifikasi destinasi yang bertindak sebagai titik hub paling strategis?</li>
</ol>
<h4>1.3 Tujuan</h4>
<ol>
  <li>Menyusun model representasi data pariwisata Pulau Bali ke dalam struktur data Graph menggunakan pendekatan Adjacency List guna memetakan hubungan antar-destinasi secara terstruktur.</li>
  <li>Mengimplementasikan algoritma Dijkstra ke dalam sistem untuk menyediakan fitur pencarian rute multi-destinasi (itinerary) terbaik yang mampu mengoptimalkan parameter jarak, estimasi waktu tempuh, maupun efisiensi biaya.</li>
  <li>Menerapkan algoritma Breadth-First Search (BFS) untuk visualisasi jangkauan eksplorasi wilayah dan memanfaatkan metrik Degree Centrality untuk menganalisis destinasi wisata yang memiliki konektivitas tertinggi sebagai titik transit strategis.</li>
  <li>Membangun sebuah aplikasi Decision Support System (DSS) interaktif berbasis web menggunakan framework Streamlit yang berhasil mengintegrasikan kecerdasan buatan (Gemini API) serta data cuaca kontekstual (real-time) guna memberikan rekomendasi perjalanan yang personal dan adaptif bagi pengguna.</li>
</ol>
<h4>1.4 Manfaat</h4>
<ol>
  <li>Membantu wisatawan merencanakan perjalanan wisata lebih matang</li>
  <li>Mengurangi resiko pemborosan sumber daya seperti biaya dan waktu</li>
  <li>Membuat pengalaman berwisata lebih nyaman untuk dilakukan</li>
  <li>Membangun sebuah aplikasi Decision Support System (DSS) interaktif berbasis web menggunakan framework Streamlit yang berhasil mengintegrasikan kecerdasan buatan (Gemini API) serta data cuaca kontekstual (real-time) guna memberikan rekomendasi perjalanan yang personal dan adaptif bagi pengguna.</li>
</ol>
<br>
<h2><bold>DASAR TEORI</bold></h2>
<h4>2.1 Sistem Pendukung Keputusan (DSS)</h4>
<p>Decision Support System (DSS) atau Sistem Pendukung Keputusan adalah sistem berbasis komputer yang interaktif, fleksibel, dan adaptif yang dikembangkan secara khusus untuk membantu manajemen atau pengguna dalam mengambil keputusan dari masalah yang tidak terstruktur atau semi-terstruktur. DSS tidak bertujuan untuk menggantikan peran pengambil keputusan, melainkan menyediakan informasi, analisis data, dan pemodelan yang rasional guna meningkatkan efektivitas pengambilan keputusan.
Dalam konteks pariwisata, DSS berfungsi sebagai smart travel planner. Wisatawan sering kali dihadapkan pada masalah semi-terstruktur, seperti memilih destinasi yang optimal di tengah keterbatasan waktu, biaya, serta faktor eksternal seperti cuaca. DSS memproses variabel-variabel tersebut menggunakan model matematis dan algoritma tertentu untuk menghasilkan rekomendasi rencana perjalanan (itinerary) yang paling efisien.</p>
<h4>2.2 Struktur Data Graph</h4>
<p>Graph adalah struktur data non-linear yang digunakan untuk merepresentasikan hubungan relasional antara sekumpulan objek. Secara matematis, sebuah graf $G$ didefinisikan sebagai pasangan himpunan $(V, E)$, di mana:$V$ adalah Vertex atau Node (titik), yang merepresentasikan objek atau entitas.$E$ adalah Edge (sisi atau garis), yang merepresentasikan hubungan atau konektivitas antara dua vertex.</p> 
<h5>2.2.1 Relevansi Graf Dalam Pemetaan Pariwisata</h5>
<p>Struktur data graf sangat cocok digunakan untuk memodelkan jaringan pariwisata karena karakteristik geografis dunia nyata memiliki kesamaan sifat fisik dengan elemen graf. Destinasi wisata, hotel, bandara, atau titik transit dapat dimodelkan secara akurat sebagai Node. Sementara itu, jalur transportasi, jalan raya, atau rute penerbangan yang menghubungkan tempat-tempat tersebut bertindak sebagai Edge.
Pemodelan linear (seperti array atau list biasa) tidak mampu menangani hubungan multi-arah dan bercabang yang ada pada jaringan jalan raya. Dengan graf, sistem dapat menghitung akumulasi bobot di sepanjang jalur untuk melakukan optimasi keputusan rute.</p>
<h5>2.2.2 Jenis graph yang digunakan</h5>
<ul>
  <li>Undirected Graph (Tidak Berarah): Sisi yang menghubungkan dua titik tidak memiliki arah khusus. Jika terdapat jalur dari Destinasi A ke Destinasi B, maka secara otomatis rute tersebut dapat dilalui dari arah sebaliknya (Destinasi B ke Destinasi A) dengan asumsi aksesibilitas jalan dua arah.</li>
  <li>Weighted Graph (Berbobot): Setiap edge memiliki nilai atau bobot (weight) tertentu. Dalam sistem pariwisata ini, bobot tersebut bersifat multi-variabel, meliputi jarak geografis (dalam kilometer), estimasi waktu tempuh (dalam menit), serta biaya transportasi (biaya bahan bakar atau tarif tol).</li>
</ul>
<h5>2.2.3 Representasi Graph (Adjacency List)</h5>
<p>Untuk mengimplementasikan graf ke dalam bahasa pemrograman Python, digunakan metode Daftar Ketenagaan (Adjacency List). Dalam pendekatan ini, graf direpresentasikan sebagai sebuah dictionary atau tabel hash, di mana setiap vertex bertindak sebagai kunci (key), dan nilainya (value) adalah sebuah daftar berisi vertex-vertex lain yang terhubung langsung dengannya beserta bobot sisinya.
Adjacency List dipilih karena memiliki efisiensi memori yang jauh lebih baik dibandingkan Adjacency Matrix, terutama untuk graf yang bersifat sparse (renggang). Pada jaringan pariwisata Bali, tidak semua tempat wisata terhubung langsung dengan semua tempat wisata lainnya, sehingga penggunaan Adjacency List menghemat ruang penyimpanan sebesar <bold>O(V+E).</bold></p>
<h4>2.3 Algoritma Penjelajahan dan Pencarian Jalur Terpendek</h4>
<h5>2.3.1 Algoritma Djikstra</h5>
<p>Algoritma Dijkstra adalah algoritma greedy yang digunakan untuk menemukan jalur terpendek (shortest path) dari satu titik sumber (single-source) ke titik-titik lainnya pada sebuah graf berbobot positif. Cara kerjanya dimulai dengan menginisialisasi jarak dari titik awal ke dirinya sendiri dengan nilai $0$ dan jarak ke semua titik lain dengan nilai tak hingga ($\infty$). Selanjutnya, semua titik dimasukkan ke dalam sebuah antrean prioritas (priority queue/min-heap) berdasarkan jarak sementaranya. Titik dengan jarak terkecil kemudian diambil dari antrean dan ditandai sebagai titik yang telah dikunjungi (visited). Setelah itu, dilakukan proses relaxation (relaksasi) terhadap semua tetangga dari titik tersebut yang belum dikunjungi, di mana jika jarak baru melalui titik ini lebih kecil daripada jarak yang tercatat sebelumnya, data jarak tersebut akan diperbarui. Proses ini terus diulangi secara berulang hingga antrean kosong atau titik tujuan telah berhasil dicapai.Jika diimplementasikan menggunakan Min-Priority Queue berbasis Binary Heap, kompleksitas waktu algoritma Dijkstra adalah $O((V + E) \log V)$, di mana $V$ adalah jumlah vertex dan $E$ adalah jumlah edge. Kompleksitas ruangnya adalah $O(V)$ untuk menyimpan tabel jarak dan status kunjungan.</p>
<h5>2.3.2 Algoritma Breadth-First Search</h5>
<p>Breadth-First Search (BFS) adalah algoritma penjelajahan graf yang melakukan pencarian secara melebar dengan mengunjungi semua node tetangga pada tingkat yang sama terlebih dahulu sebelum berpindah ke node di tingkat berikutnya. Cara kerjanya memanfaatkan struktur data antrean (Queue) yang menganut prinsip First-In, First-Out (FIFO), di mana proses pencarian dimulai dari node akar yang dimasukkan ke dalam queue lalu ditandai sebagai lokasi yang sudah dikunjungi. Selama antrean tersebut tidak kosong, elemen terdepan akan dikeluarkan dari queue untuk diperiksa, dan seluruh node tetangganya yang belum pernah dikunjungi akan dimasukkan ke dalam antrean secara berurutan. Dalam sistem ini, BFS diimplementasikan untuk melakukan simulasi jangkauan atau eksplorasi wilayah pariwisata secara bertahap dari satu titik lokasi awal yang ditentukan oleh pengguna tanpa memedulikan bobot nilai pada rute.Kompleksitas waktu dari algoritma BFS ini adalah $O(V + E)$ karena setiap titik (vertex) dan sisi (edge) di dalam jaringan graf pariwisata akan diperiksa tepat satu kali selama proses penjelajahan berlangsung. Sementara itu, kompleksitas ruang yang dibutuhkan adalah $O(V)$ yang dialokasikan khusus untuk menyimpan data antrean serta daftar status kunjungan dari seluruh node yang ada di dalam sistem.</p>
<h4>2.4 Analisis Sentralitas</h4>
<p>Degree Centrality adalah salah satu metrik paling mendasar dalam analisis jaringan (Network Analysis) untuk mengukur tingkat kepentingan atau keterpautan suatu node di dalam graf. Nilai sentralitas derajat sebuah node ditentukan langsung oleh jumlah edge yang terhubung langsung dengannya (derajat node tersebut).Secara matematis, untuk graf tidak berarah, nilai Degree Centrality yang dinormalisasi ($C_D$) dari sebuah vertex $v$ dirumuskan sebagai:$$C_D(v) = \frac{\text{deg}(v)}{|V| - 1}$$Di mana $\text{deg}(v)$ adalah derajat dari vertex $v$, dan $|V|$ adalah total jumlah vertex dalam graf.Dalam DSS pariwisata, destinasi yang memiliki nilai Degree Centrality tertinggi diidentifikasi sebagai titik transit strategis (hub). Tempat wisata atau lokasi dengan nilai sentralitas tinggi menandakan bahwa lokasi tersebut memiliki aksesibilitas geografis terbaik karena terhubung langsung dengan banyak rute alternatif, sehingga sangat ideal direkomendasikan sebagai titik awal keberangkatan atau lokasi penginapan selama liburan.</p>
<h4>2.5 Integrasi Application Programming Interface (API)</h4>
Untuk mendukung proses pengambilan keputusan yang dinamis dan relevan, DSS ini mengintegrasikan dua jenis layanan API pihak ketiga:
<dl>
  <dt>Gemini API</dt>
  <dd>Gemini API merupakan layanan kecerdasan buatan berbasis Large Language Model (LLM). Dalam sistem ini, Gemini API bertindak sebagai generator rekomendasi berbasis bahasa alami. Data hasil perhitungan matematis algoritma Dijkstra (berupa urutan lokasi, akumulasi jarak, dan biaya) dikirimkan sebagai prompt ke model AI untuk diolah menjadi teks narasi rekomendasi perjalanan berbahasa Indonesia yang interaktif, personal, dan mudah dipahami oleh pengguna awam.</dd>
  <dt>OpenWeatherMap API</dt>
  <dd>OpenWeatherMap API digunakan untuk menyediakan data cuaca terkini (real-time weather data) pada koordinat geografis Pulau Bali. Informasi cuaca seperti suhu, kelembapan, dan status hujan diintegrasikan ke dalam logika DSS untuk memberikan saran adaptif. Jika suatu wilayah terdeteksi mengalami cuaca buruk atau hujan, sistem secara otomatis akan memberikan catatan khusus atau menyesuaikan prioritas rekomendasi ke arah destinasi wisata indoor (seperti museum atau pertunjukan seni) demi kenyamanan wisatawan.</dd>
</dl>
<h2>BAB III: Analisis dan Perancangan</h2>

<h4>3.1 Analisis Masalah</h4>
<p>Saat berlibur ke Bali, wisatawan sering menghadapi masalah klasik: bingung menyusun jadwal perjalanan (itinerary). Masalah utama yang sering muncul antara lain:</p>
<ul>
    <li><strong>Information Overload:</strong> Terlalu banyak pilihan tempat wisata membuat wisatawan bingung harus mulai dari mana.</li>
    <li><strong>Pemborosan Waktu & Biaya:</strong> Rute yang acak-acakan bikin waktu habis di jalan dan bensin terkuras karena jalurnya tumpang tindih.</li>
    <li><strong>Faktor Tak Terduga:</strong> Sudah sampai di lokasi terbuka (outdoor) tapi ternyata hujan deras, sehingga liburan jadi kurang maksimal.</li>
</ul>
<p>Sistem Pendukung Keputusan (DSS) ini dibuat untuk menyelesaikan masalah tersebut. Dengan memasukkan preferensi seperti budget, waktu tempuh, dan kategori wisata favorit, sistem akan otomatis menghitung dan memberikan rekomendasi rute perjalanan yang paling efisien.</p>

<h4>3.2 Desain Graf (Node dan Edge)</h4>
<p>Untuk memodelkan jaringan pariwisata di Bali, sistem ini mengubah peta dunia nyata menjadi struktur data Graf Tidak Berarah dan Berbobot (Weighted Undirected Graph). Pemodelannya dirancang sebagai berikut:</p>
<ul>
    <li><strong>Node (Titik):</strong> Merepresentasikan destinasi wisata, hotel, atau titik awal keberangkatan. Setiap node menyimpan data penting seperti nama tempat, kategori (pantai, pura, alam, dll), rating bintang, koordinat lokasi, dan harga tiket masuk.</li>
    <li><strong>Edge (Sisi/Garis):</strong> Merepresentasikan jalan raya atau rute yang menghubungkan antar destinasi. Setiap edge memiliki tiga jenis bobot (weight) yang bisa dipilih pengguna untuk optimasi: jarak (km), waktu tempuh (menit), dan biaya transportasi.</li>
    <li><strong>Representasi Kode:</strong> Di dalam kode Python, graf ini disimpan menggunakan format <strong>Adjacency List</strong> berbasis Dictionary. Format ini dipilih karena sangat ringan dan cepat saat proses pencarian rute dibanding menggunakan matriks biasa.</li>
</ul>

<h4>3.3 Alur Kerja Sistem</h4>
<p>Secara sederhana, cara kerja aplikasi ini dibagi menjadi empat tahapan utama:</p>
<ol>
    <li><strong>Input Pengguna:</strong> Melalui antarmuka Streamlit, pengguna memilih lokasi awal, destinasi tujuan, kategori wisata yang disukai, batasan maksimal budget, serta parameter optimasi yang diinginkan (jarak/waktu/biaya).</li>
    <li><strong>Penyaringan & Pemrosesan Graf (Graph Engine):</strong> Sistem akan memfilter node berdasarkan kategori pilihan. Selanjutnya, Algoritma Dijkstra bekerja mencari jalur dengan bobot terkecil, BFS mensimulasikan jangkauan wilayah, dan Degree Centrality mendeteksi titik transit paling strategis.</li>
    <li><strong>Pengayaan Data (API Integration):</strong> Jalur matematis yang sudah ketemu akan digabungkan dengan informasi cuaca real-time dari OpenWeatherMap API untuk melihat apakah lokasi tujuan aman dari hujan. Setelah itu, semua data dikirim ke Gemini API (AI) untuk diubah menjadi narasi tips perjalanan.</li>
    <li><strong>Output Visual:</strong> Pengguna menerima hasil akhir di dashboard berupa peta graf interaktif (Plotly), ringkasan total biaya dan waktu, serta teks panduan liburan yang ditulis langsung oleh AI.</li>
</ol>
<h2>BAB IV: Implementasi</h2>

<h4>4.1 Lingkungan Pengembangan</h4>
<p>Aplikasi ini dibangun menggunakan bahasa pemrograman Python karena fleksibilitasnya dalam menangani struktur data dan integrasi API. Untuk antarmuka penggunanya (UI), sistem ini menggunakan framework <strong>Streamlit</strong>. Streamlit dipilih karena memungkinkan pembuatan <i>dashboard</i> interaktif berbasis web dengan cepat tanpa perlu repot mengatur HTML/CSS dari awal[cite: 1, 11].</p>

<h4>4.2 Pembuatan Graf dan Logika Algoritma</h4>
<p>Implementasi logika utama berada pada modul pengolah graf. Berikut adalah bagaimana komponen-komponen tersebut bekerja di dalam sistem:</p>
<ul>
    <li><strong>Data Loader:</strong> Sistem membaca data dari file JSON (nodes.json dan edges.json) yang berisi daftar tempat wisata dan jalur penghubungnya[cite: 101]. Data ini kemudian dirakit menjadi objek graf.</li>
    <li><strong>Dijkstra untuk Rute:</strong> Algoritma Dijkstra diimplementasikan untuk mencari rute. Ketika pengguna memilih titik awal dan tujuan, algoritma ini akan menghitung bobot kumulatif terkecil (bisa berupa jarak, waktu, atau biaya)[cite: 114, 115].</li>
    <li><strong>Multi-Stop Planning:</strong> Untuk rencana liburan dengan banyak destinasi, sistem menggunakan pendekatan <i>Greedy</i> yang digabungkan dengan Dijkstra agar rute yang dipilih tidak melebihi batas budget yang dimasukkan pengguna[cite: 140, 142, 143].</li>
</ul>

<h4>4.3 Integrasi API (Cuaca dan AI)</h4>
<p>Sistem ini tidak hanya bekerja dengan angka matematika, tapi juga data dari dunia nyata:</p>
<ul>
    <li><strong>OpenWeatherMap API:</strong> Sistem menarik data cuaca Kota Denpasar secara <i>real-time</i>[cite: 183]. Jika cuaca sedang hujan, sistem akan mengetahuinya dan menyiapkan peringatan[cite: 185, 189].</li>
    <li><strong>Gemini AI:</strong> Hasil hitungan rute dari Dijkstra, sisa budget, dan data cuaca tersebut tidak langsung ditampilkan begitu saja. Data mentah ini dikemas dan dikirim ke Gemini AI[cite: 81, 88]. AI kemudian meracik data tersebut menjadi paragraf sapaan dan tips liburan berbahasa Indonesia yang hangat dan mudah dibaca[cite: 80, 83].</li>
</ul>


<h2>BAB V: Pengujian dan Analisis</h2>

<h4>5.1 Skenario Pengujian</h4>
<p>Untuk memastikan sistem berjalan dengan baik, dilakukan pengujian menggunakan berbagai skenario preferensi wisatawan. Misalnya, skenario wisatawan dengan "Budget Terbatas" versus "Budget Sultan", atau skenario prioritas "Waktu Tercepat" versus "Jarak Terpendek".</p>

<h4>5.2 Analisis Hasil Pencarian Rute (Dijkstra)</h4>
<p>Dari hasil pengujian, algoritma Dijkstra terbukti berhasil menemukan jalur yang sesuai dengan kriteria yang diminta. Ketika pengguna memasukkan batas budget yang ketat, fitur <i>Multi-Stop Planning</i> berhasil menghentikan penambahan destinasi ketika total biaya perjalanan (transportasi dan tiket masuk) sudah hampir menyentuh batas maksimal[cite: 143]. Perhitungan jarak dan waktunya pun sangat akurat berdasarkan bobot <i>edge</i> yang dimasukkan.</p>

<h4>5.3 Analisis Output Kecerdasan Buatan (AI)</h4>
<p>Integrasi dengan Gemini AI dan OpenWeatherMap terbukti menjadi nilai tambah yang sangat besar (DSS yang sesungguhnya). AI tidak berhalusinasi (ngarang) karena panduannya dibatasi oleh hasil perhitungan algoritma[cite: 84, 85]. Selain itu, ketika API cuaca mendeteksi status "Hujan", AI dengan pintar menyesuaikan narasinya untuk menyarankan pengunjung berteduh atau mencari destinasi di dalam ruangan (indoor)[cite: 82, 92].</p>


<h2>BAB VI: Kesimpulan dan Saran</h2>

<h4>6.1 Kesimpulan</h4>
<p>Berdasarkan hasil perancangan, implementasi, dan pengujian, dapat ditarik kesimpulan bahwa:</p>
<ol>
    <li>Struktur data Graf (Adjacency List) terbukti sangat efektif untuk memodelkan jaringan pariwisata di Bali, di mana titik wisata menjadi <i>Node</i> dan jalur transportasi menjadi <i>Edge</i>.</li>
    <li>Algoritma Dijkstra berhasil diterapkan untuk memecahkan masalah pencarian rute wisata yang paling efisien berdasarkan batasan waktu, jarak, dan biaya pengguna.</li>
    <li>Penggabungan antara komputasi graf, metrik <i>Degree Centrality</i>, serta kecerdasan buatan (Gemini AI) menghasilkan sebuah Sistem Pendukung Keputusan (DSS) yang interaktif, cerdas, dan adaptif terhadap kondisi di lapangan (seperti cuaca).</li>
</ol>

<h4>6.2 Saran</h4>
<p>Untuk pengembangan sistem selanjutnya, ada beberapa hal yang bisa ditingkatkan:</p>
<ul>
    <li><strong>Data Real-Time Traffic:</strong> Ke depannya, bobot waktu tempuh pada <i>edge</i> sebaiknya menggunakan API peta (seperti Google Maps API) agar kemacetan lalu lintas asli di Bali bisa ikut terhitung.</li>
    <li><strong>Penambahan Database:</strong> Menambah variasi destinasi wisata (node) yang lebih banyak, termasuk tempat makan lokal atau penginapan, agar variasi rencana perjalanan (itinerary) yang dihasilkan AI menjadi lebih kaya.</li>
</ul>
<div></div>

https://canva.link/slcovofayhkjz0q Link PPT Presentasi
https://youtu.be/7fB82Q8e00E link video demo (YT)
