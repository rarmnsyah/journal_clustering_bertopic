import string
import re

def bersihkan_abstrak(teks):
    teks = teks.lower()
    
    # Membagi teks berdasarkan kata "ABSTRAK"
    abstrak_bersih = re.split(r'abstrak|abstract', teks)[-1].strip()

    # Membagi teks hasil pemisahan dengan menggunakan '\n' untuk mendapatkan baris-baris yang terpisah
    baris = re.split(r'\n|\.\s|\.', abstrak_bersih)

    # Menggabungkan baris-baris yang tersisa kembali menjadi teks yang bersih
    abstrak_bersih = ' '.join(baris).strip()

    # Menghapus tag nbsp pada text
    abstrak_bersih = abstrak_bersih.replace("&nbsp;", '')

    # Menghapus simbol spesial yang ada pada text
    abstrak_bersih = abstrak_bersih.translate(str.maketrans('', '', 'å¼«¥ª°©ð±œ§µ½ºé/èšˆçžãƒÿ¾æ¹¢³¿β®äâ£'))

    # Hanya mengambil huruf alphanumeric
    abstrak_bersih = re.sub(r'[^ \w+]', '', abstrak_bersih)

    # Filtering angka
    abstrak_bersih = re.sub('\d+', '', abstrak_bersih)

    # menghapus punctuation pada teks
    abstrak_bersih = abstrak_bersih.translate(str.maketrans('', '', string.punctuation))

    # seluruh karakter setelah kata kunci ‘kata kunci|keywords|keyword’
    abstrak_bersih = re.sub('(kata kunci|keywords|keyword).*', '', abstrak_bersih)

    return abstrak_bersih