import os
import pysam
import pandas as pd
import datetime as date

print(f"Assurez-vous que les fichiers BAM, VCF et BED soient dans le même répertoire que le script CosmicNavigatorVador.py et évitez les raccourcis.")

# Vérification de l'existence du fichier de sortie
file_name = "cnv_listing_" + date_string + ".csv"
if os.path.isfile(file_name):
    while True:
        overwrite = input("Le fichier de sortie existe déjà. Souhaitez-vous l'écraser ? (Oui/Non) ")
        if overwrite.lower() == "oui":
            break
        elif overwrite.lower() == "non":
            i = 1
            while True:
                new_file_name = file_name.split(".")[0] + f" ({i}).csv"
                if not os.path.isfile(new_file_name):
                    file_name = new_file_name
                    break
                i += 1
            break
        else:
            print("Réponse non valide. Veuillez répondre par 'oui' ou par 'non'.")

# Recherche des fichiers d'entrées
bam_file = None
vcf_file = None
bed_file = None
for file in os.listdir('.'):
    if file.endswith('.bam'):
        bam_file = file
    elif file.endswith('.vcf'):
        vcf_file = file
    elif file.endswith('.bed'):
        bed_file = file

#Vérification des extensions de fichiers
if not bam_file:
    raise ValueError("Fichier BAM non retrouvé. Le fichier BAM doit avoir une extension .bam")
if not vcf_file:
    raise ValueError("Fichier VCF non retrouvé. Le fichier VCF doit avoir l'extension .vcf")
if not bed_file:
    raise ValueError("Fichier BED non retrouvé. Le fichier BED doit avoir l'extension .bed")

# Vérification que le contenu des fichiers correspond aux extensions
try:
    with open(bam_file, 'rb') as f:
        header = f.read(4)
        if header != b'BAM\1':
            raise ValueError("Le fichier BAM n'est pas valide. Il peut être soit tronqué, soit corrompu.")
except ValueError as e:
    raise e

try:
    with open(vcf_file, 'r') as f:
        first_line = f.readline()
        if not first_line.startswith("##fileformat=VCF"):
            raise ValueError("Le fichier VCF n'est pas valide. Il peut être soit tronqué, soit corrompu.")
except ValueError as e :
    raise e

try:
    with open(bed_file, 'r') as f:
        f.readline()
        f.readline()
        if not f.readline().startswith("chr"):
            raise ValueError("Le fichier BED n'est pas valide. Il peut être soit tronqué, soit corrompu.")
except ValueError as e:
    raise e

# Ouverture des fichiers d'entrée en utilisant pysam pour le fichier bam et pandas pour les fichiers VCF et BED
# On utilise l'argument reference_filename pour spécifier que la base de données soit celle de l'Homme en Grch37
bam = pysam.AlignmentFile(bam_file, "rb", reference_filename="I:\MME PLANCKE\Sauvegarde Bioinfo\Human_v37.p13_105\allContigs.fa")
# On utilise l'argument skiprows pour sauter les 28 premières lignes qui sont des entêtes dans le fichier vcf
vcf = pd.read_csv(vcf_file, sep='\t', header=None, skiprows=28)
bed = pd.read_csv(bed_file, sep='\t', header=None)

# Initialisation de la liste pour stocker les CNV
cnvs = []

# Boucle pour parcourir les entrées du fichier BAM
for read in bam.fetch():
    # Récupération des informations sur la CNV à partir du fichier BAM
    chrom = read.reference_name
    start = read.reference_start
    end = read.reference_end
    cnv_length = end - start
    # Recherche de la CNV dans le fichier VCF
    vcf_match = vcf[(vcf[0] == chrom) & (vcf[1] >= start) & (vcf[1] <= end)]
    if vcf_match.empty:
        # Si aucun match n'est trouvé, recherche de la CNV dans le fichier BED
        bed_match = bed[(bed[0] == chrom) & (bed[1] <= start) & (bed[2] >= end)]
        if bed_match.empty:
            # Si aucun match n'est trouvé, la CNV est considérée comme non répertoriée
            cnv_type = "non répertoriée"
        else:
            # Si un match est trouvé dans le fichier BED, récupération de la classe de la CNV
            cnv_type = bed_match.iloc[0][3]
    else:
        # Si un match est trouvé dans le fichier VCF, récupération de la classe de la CNV
        cnv_type = vcf_match.iloc[0][4]
    # Ajout des informations sur la CNV à la liste
    cnvs.append([chrom, start, end, cnv_length, cnv_type])

# Conversion de la liste en DataFrame de pandas
cnv_df = pd.DataFrame(cnvs, columns=["chrom", "start", "end", "length", "type"])

# Normalisation des données
cnv_df["length"] = cnv_df["length"] / cnv_df["length"].sum()

# Ajout de la date dans une variable
date_string = date.datetime.now().strftime("%Y%m%d")

# Ecriture du fichier CSV en sortie
cnv_df.to_csv(file_name, index=False)
