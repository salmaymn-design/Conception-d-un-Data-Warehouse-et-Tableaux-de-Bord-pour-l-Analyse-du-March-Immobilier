import subprocess
import sys

print("=" * 50)
print("DARKOM ETL PIPELINE")
print("=" * 50)

try:
    print("\n[1/3] Chargement des données brutes...")
    subprocess.run(
        [sys.executable, "staging/load_raw.py"],
        check=True
    )

    print("\n[2/3] Nettoyage des données...")
    subprocess.run(
        [sys.executable, "clean/clean_raw.py"],
        check=True
    )

    print("\n[3/3] Chargement Data Warehouse...")
    subprocess.run(
        [sys.executable, "warhouse/load_warhouse.py"],
        check=True
    )

    print("\nETL terminé avec succès ✅")

except subprocess.CalledProcessError as e:
    print(f"\nErreur dans une étape : {e}")