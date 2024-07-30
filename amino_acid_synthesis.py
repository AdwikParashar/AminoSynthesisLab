from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw

# Define a function to display a molecule and save it to a file
def display_and_save_molecule(mol, filename, title):
    if mol is not None:
        img = Draw.MolToImage(mol)
        img.save(filename)
        print(f"{title} molecule created and saved as {filename}.")
    else:
        print(f"Failed to create {title} molecule.")

# Define the SMILES strings for some amino acids
amino_acids_smiles = {
    "glycine": "NCC(=O)O",
    "alanine": "CC(C(=O)O)N",
    "serine": "C(C(C(=O)O)N)O",
    "tryptophan": "N[C@@H](C(O)=O)Cc1c[nH]c2ccccc12"
}

# Create the molecule objects for the amino acids
amino_acids = {name: Chem.MolFromSmiles(smiles) for name, smiles in amino_acids_smiles.items()}

# Display and save the amino acids
for name, mol in amino_acids.items():
    display_and_save_molecule(mol, f"{name}.png", name.capitalize())

# Define some chemical reactions using SMARTS strings
reactions = {
    "N-acetylation": AllChem.ReactionFromSmarts('[N:1]>>[N:1]C(=O)C'),
    "O-methylation": AllChem.ReactionFromSmarts('[OH:1]>>[O:1]C'),
    "decarboxylation": AllChem.ReactionFromSmarts('[C:1](=O)[O:2]>>[H][C:1][H]')
}


for aa_name, mol in amino_acids.items():
    for rxn_name, reaction in reactions.items():
        try:
            products = reaction.RunReactants((mol,))
            if products:
                product = products[0][0]
                product.UpdatePropertyCache()
                display_and_save_molecule(product, f"{aa_name}_{rxn_name}.png", f"{aa_name.capitalize()}_{rxn_name}")
            else:
                print(f"Reaction {rxn_name} failed for {aa_name}.")
        except Exception as e:
            print(f"An error occurred during {rxn_name} for {aa_name}: {e}")


import os
print("Current working directory:", os.getcwd())


print("Files in current directory:", os.listdir(os.getcwd()))
