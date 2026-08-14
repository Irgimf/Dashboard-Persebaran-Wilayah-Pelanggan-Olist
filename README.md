# Dashboard Persebaran Wilayah Pelanggan Olist ✨

Proyek akhir kelas *Belajar Analisis Data dengan Python* (Dicoding), menganalisis persebaran wilayah pelanggan pada E-Commerce Public Dataset (Olist Brazil).

## Setup Environment - Anaconda

```
conda create --name main-ds python=3.11
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal

```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run Notebook

Notebook analisis lengkap ada di `notebook.ipynb`. Jalankan dengan Jupyter:

```
jupyter notebook notebook.ipynb
```

Pastikan folder `data/` (berisi `customers_dataset.csv` dan `geolocation_dataset.csv`) berada satu level dengan `notebook.ipynb`.

## Run Streamlit App

```
cd dashboard
streamlit run dashboard.py
```

Pastikan file `main_data.csv` berada satu folder dengan `dashboard.py` (sudah disertakan di folder `dashboard/`).

Dashboard akan terbuka otomatis di browser pada `http://localhost:8501`.
