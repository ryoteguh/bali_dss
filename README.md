<h1><bold>Laporan SIstem Pendukung Keputusan (Decision Support System/DSS) di Pariwisata Bali</bold></h1>
<h4>Nama|NIM|akun GitHub</h4>
<ol>
  <li>Rio Teguh Priyo Utomo |2501010063| ryoteguh</li>
  <li>Ngakan Gede Marvyn Cakra Ajidharma |2501010078| marpinleclerc-jpg</li>
  <li>Andi Pratama |2501010092| eyka0209akssjjs0209</li>
</ol>
<br>
<h2><bold>PPENDAHULUAN</bold></h2>
<h4>Latar Belakang</h4>
<p>Pulau Bali adalah salah satu destinasi populer yang ada di Indonesia. Setiap tahunnya ada jutaan wisatawan dari luar maupun dalam negeri yang berkunjung untuk mencari destinasi wisata yang berbeda-beda seperti wisata budaya, pantai maupun kuliner. Namun,melimpahnya opsi destinasi ini sering kali menimbulkan fenomena <italic>information overload</italic> bagi wisatawan. Mereka kerap mengalami kesulitan dalam merencanakan rute perjalanan yang efektif, efisien, dan sesuai dengan kondisi personal mereka. Wisatawan cenderung memilih destinasi secara acak tanpa mempertimbangkan jarak geografis yang optimal, biaya, dan faktor cuaca yang menyebabkan pemborosan waktu akibat jalur yang tidak efisien, boros biaya, dan ketidaknyamanan dalam berwisata. Oleh karena itu dibutuhkan sebuah sistem modern yang dapat membantu para wisatawan membuat keputusan lebih baik.</p>
<p>Di sistem ini struktur data graph dapat digunakan untuk mengatasi pemilihan jalur transportasi dengan menggambarkan destinasi wisata dan titik keberangkatan sebagai titik <italic>node</italic> dan jalur yang menghubungkan setiap titik sebagai <italic>edge</italic>. Lalu hubungan antar destinasi diberi bobot seperti jarak biaya dan waktu agar pemilihan jalur lebih akurat. Penggunaan algoritma <italic>Djikstra</italic> akan membantu pemilihan jalur karena mampu mengevaluasi bobot untuk mencari jalur terpendek. Selain itu algoritma Breadth-First Search juga digunakan untuk mengetahui jangkauan wilayah wisata dan menentukan titik destinasi yang strategis. Namun hasil dari keputusan algoritma biasanya kaku dan sulit dipahami oleh orang awam. Maka dari itu sistem ini akan diimplementasikan dalam bentuk web dengan kecerdasan buatan Gemini AI dan pemantauan cuaca real-time menggunakan OpenWeatherMap API. </p>
<p>Berdasarkan diskusi tersebut, maka ditetapkan projek ini adalah projek membuat <strong>Sistem Pendukung Keputusan (Decision Support System/DSS) Pariwisata Bali berbasis graf</strong>. Sistem ini diharapkan dapat membantu wisatawan menyusun perencanaan wisata lebih baik,mengurangi resiko pemborosan sumber daya waktu dan biaya, serta mengimplementasikan konsep struktur data graf pada kasus di dunia nyata.</p>
<h2></h2>
