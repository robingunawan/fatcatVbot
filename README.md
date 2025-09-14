clone repo:

git clone https://github.com/robingunawan/fatcatVbot.git
cd fatcatVbot


lihat isi file penting:

ls -la
sed -n '1,200p' requirements.txt      # lihat dependency python
sed -n '1,200p' sample.env             # lihat template env
sed -n '1,200p' installnode.sh         # script instal node (kalau ada)
sed -n '1,200p' cookies.txt            # *PERINGATAN: file sensitif — lihat saja, jangan commit lagi*


cek apakah ada package.json (untuk Node) dan skrip start:

ls | grep package.json || echo "no package.json"
sed -n '1,200p' start


cari file yang berisi token/kata “secret” (quick grep):

grep -RIn "token\|api_key\|secret\|COOKIE\|BOT_TOKEN" .


Jika ada hasil yang berisi kredensial nyata — segera hapus dari repo dan rotasi credential tersebut (ganti token di layanan terkait).

jalankan instalasi environment (Python):

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


Perhatikan error saat pip install — biasanya muncul versi paket yang tidak cocok atau paket yang hilang.

coba jalankan bot (ikuti README; dari README terlihat perintah):

cp sample.env .env
# edit .env sesuai kebutuhan
python3 -m PyroUbot
