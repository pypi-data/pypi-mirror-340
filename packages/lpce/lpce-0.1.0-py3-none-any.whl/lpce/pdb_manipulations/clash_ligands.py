import sys
from pathlib import Path

import numpy as np
from Bio.PDB import PDBIO, PDBParser, Select
from joblib import Parallel, delayed
from loguru import logger
from tqdm import tqdm

logger.remove()
logger.add(sys.stdout, format="{message}", level="INFO")


class LigandSelect(Select):
    def __init__(self, ligand_residues):
        self.ligand_residues = ligand_residues

    def accept_residue(self, residue):
        # Сохраняем белок и выбранный лиганд
        if residue in self.ligand_residues or residue.id[0].strip() == "":
            return True
        return False


def split_overlapping_ligands_in_file(pdb_file, distance_cutoff=0.5):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("complex", pdb_file)

    # Собираем лиганды
    ligands = []
    for model in structure:
        for chain in model:
            for residue in chain:
                hetfield = residue.id[0].strip()
                if hetfield != "" and hetfield != "W":
                    ligands.append(residue)

    # Если меньше двух лигандов, нет смысла проверять
    if len(ligands) < 2:
        return [], pdb_file.name

    overlapping_ligands = set()
    # Проверяем все пары лигандов
    for i in range(len(ligands)):
        ligand1_atoms = list(ligands[i].get_atoms())
        for j in range(i + 1, len(ligands)):
            ligand2_atoms = list(ligands[j].get_atoms())

            # Вычисляем расстояния между атомами
            for atom1 in ligand1_atoms:
                coord1 = atom1.get_coord()
                for atom2 in ligand2_atoms:
                    coord2 = atom2.get_coord()
                    distance = np.linalg.norm(coord1 - coord2)
                    if distance < distance_cutoff:
                        # Обнаружено наложение лигандов
                        overlapping_ligands.update([ligands[i], ligands[j]])
                        break  # Достаточно найти одну пару атомов
                else:
                    continue
                break

    if overlapping_ligands:
        # Для каждого накладывающегося лиганда создаем отдельный файл
        output_files = []
        for ligand in overlapping_ligands:
            io = PDBIO()
            io.set_structure(structure)
            ligand_select = LigandSelect([ligand])
            ligand_name = ligand.get_resname()
            ligand.get_parent().id

            # Изменяем имя файла, заменяя оригинальный HET код на название текущего лиганда
            original_filename = pdb_file.name
            # Находим индекс начала и конца HET кода в имени файла
            start_idx = original_filename.find("bioml_")
            if start_idx != -1:
                start_idx += len("bioml_")
                # Находим номер bioml
                bioml_number = ""
                while original_filename[start_idx].isdigit():
                    bioml_number += original_filename[start_idx]
                    start_idx += 1
                # Теперь находим начало HET кода
                het_start_idx = start_idx + 1  # Пропускаем символ '_'
                het_end_idx = original_filename.find("_chains", het_start_idx)
                if het_end_idx != -1:
                    # Формируем новое имя файла
                    new_filename = (
                        original_filename[:het_start_idx]
                        + ligand_name
                        + original_filename[het_end_idx:]
                    )
                else:
                    # Если не удалось найти '_chains', используем оригинальное имя файла
                    new_filename = original_filename
            else:
                # Если не удалось найти 'bioml_', используем оригинальное имя файла
                new_filename = original_filename

            output_path = pdb_file.parent / new_filename
            io.save(str(output_path), ligand_select)
            output_files.append(new_filename)
        # Удаляем оригинальный файл
        pdb_file.unlink()
        return output_files, pdb_file.name
    else:
        # Наложений не найдено
        return [], pdb_file.name


def process_structures(output_dir, distance_cutoff=0.5, n_jobs=1):
    pdb_files = list(Path(output_dir).glob("*.pdb"))

    logger.info("\n======== Splitting files with overlapping ligands ========")

    results = Parallel(n_jobs=n_jobs)(
        delayed(split_overlapping_ligands_in_file)(pdb_file, distance_cutoff)
        for pdb_file in tqdm(pdb_files)
    )

    split_files = []
    processed_files = []
    for new_files, original_name in results:
        if new_files:
            split_files.extend(new_files)
            processed_files.append(original_name)

    logger.info(f"Total files processed: {len(pdb_files)}")
    logger.info(f"Files with split ligands: {len(processed_files)}")
    logger.info(f"Created new files: {len(split_files)}")
    logger.debug(f"New files: {split_files}")

    return {"split_files": split_files}


def split_overlapping_ligands(cfg):
    return process_structures(
        output_dir=cfg.paths.separated_dir,
        distance_cutoff=cfg.overlapping.overlapping_threshold,
        n_jobs=cfg.n_jobs,
    )
