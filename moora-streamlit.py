import streamlit as st
import numpy as np

from pyDecision.algorithm import moora_method

st.write('Hasil Perangkingan dengan Metode MOORA')

# Input jumlah bobot
num_weights = 5

# Masukkan bobot
weights = []
kriteria = ['RAM','HDD','HARGA','BERAT','PROSESOR']
st.write('Masukkan Bobot:')
for i in range(num_weights):
    weight = st.number_input(f'Bobot {kriteria[i+1]}', value=0.0, step=0.01)
    weights.append(weight)

# Load Criterion Type: 'max' or 'min'
criterion_type = []
st.write('Pilih Tipe Kriteria:')
for i in range(num_weights):
    criterion = st.selectbox(f'Kriteria {i+1}', options=['max', 'min'])
    criterion_type.append(criterion)

# Input nama alternatif
st.write('Masukkan Nama Alternatif:')
alternative_labels = []
i = 0
while True:
    label = st.text_input(f'Alternatif {i+1}')
    if label.strip() == '':  # Cek jika input kosong
        break
    alternative_labels.append(label)
    i += 1

# Dataset
dataset = []
for _ in range(len(alternative_labels)):
    st.subheader(f'Masukkan atribut untuk Alternatif {alternative_labels[_]}')
    attributes = []
    for i in range(num_weights):
        attribute = st.number_input(f'Atribut {i+1} untuk {alternative_labels[_]}', value=0, step=10)
        attributes.append(attribute)
    dataset.append(attributes)

# Tombol untuk melakukan perhitungan
if st.button('Hitung Perangkingan') and len(alternative_labels) >= 2:
    dataset = np.array(dataset)

    # Call MOORA Function
    rank = moora_method(dataset, weights, criterion_type, graph=True, verbose=True)
    ranks = [item[0] for item in rank]
    int_ranks = [int(item[0]) for item in rank]

    scores = [item[1] for item in rank]
    sorted_scores = sorted(scores, reverse=True)
    #reversed_scores = scores[::-1]

    # Creating a table with only scores
    result_table = {'Alternatif': alternative_labels, 'Peringkat': int_ranks}

    sorted_table = sorted(zip(result_table['Alternatif'], result_table['Peringkat']), key=lambda x: x[1])
    sorted_alternatif, sorted_ranks = zip(*sorted_table)
    sorted_result_table = {'Alternatif': list(sorted_alternatif), 'Skor': list(sorted_scores), 'Peringkat': list(sorted_ranks)}

    #combined_data = []
    #for score, alt, rank in zip(sorted_scores, sorted_result_table['Alternatif'], sorted_result_table['Peringkat']):
    #  combined_data.append({'Alternatif': alt, 'Peringkat': rank, 'Score': score})

    #st.write('Hasil Perangkingan:')
    #st.write(combined_data)

    # Dipake Nanti Kalo Gagal
    # Menampilkan hasil perangkingan ke dalam antarmuka Streamlit dalam bentuk tabel
    # result_table = {'Alternatif': alternative_labels, 'Peringkat': ranks}
    # Reversing the order of alternative labels
    # reversed_scores = scores[::-1]

    # Creating a new dictionary with reversed labels
    # reversed_result_table = {'Alternatif': alternative_labels, 'Nilai': reversed_scores, 'Peringkat': ranks}

    st.write('Hasil Perangkingan:')
    st.table(sorted_result_table)
    #st.table(sorted_scores)
    #st.table(reversed_result_table)

    lowest_rank_index = 0  # Mengambil indeks pertama untuk peringkat terendah
    alternatif_lowest_rank = sorted_alternatif[lowest_rank_index]

    st.write(f"Kesimpulan: Rekomendasi laptop untuk dibeli adalah {alternatif_lowest_rank}")

else:
    st.warning("Masukkan setidaknya dua nama alternatif untuk melakukan perangkingan.")

