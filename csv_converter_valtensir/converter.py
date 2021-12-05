import logging
from pathlib import Path
import click
import json


logging.basicConfig(
    level="DEBUG", format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

@click.command()

@click.option(
    "--convert",
    "-c",
    default="cc",
    help="Format you want to convert. cc -> Convert CSV to JSON; cj -> Convert JSON to CSV."
)

@click.option(
    "--input", 
    "-i", 
    default="./", 
    help="Path where to find the files to convert.", 
    type=str
)

@click.option(
    "--output", 
    "-o", 
    default="./", 
    help="Path where the converted files will be saved.", 
    type=str
)

@click.option(
    "--delimiter", 
    "-d", 
    default=",", 
    help="Separator used to split the files.", 
    type=str
)

@click.option(
    "--prefix", 
    "-p",
    prompt=True,
    prompt_required=False, 
    default="file", 
    help=("Prefix used to prepend to the name of the converted file saved on disk."
        "The suffix will be a number starting from 0. ge: file_0"
    ),
)
def converter(convert: str="cc", input: str="./", output: str="./", delimiter: str=",", prefix: str=None):
    input_path = Path(input)
    output_path = Path(output)

    for p in [input_path, output_path]:
        if not (p.is_file() or p.is_dir):
            raise TypeError("Not a valid path of file name.")

    if convert == "cc":    
        data = read_csv_file(source=input_path, delimiter=delimiter)
        save_to_json_file(csvs=data, output_path=output_path, prefix=prefix, delimiter=delimiter)
    elif convert == "cj":
        data = read_csv_file(source=input_path, delimiter=delimiter)
        save_to_json_file(csvs=data, output_path=output_path, prefix=prefix, delimiter=delimiter)
    else:
        raise TypeError("Not a valid file format")



def read_csv_file(source: Path, delimiter: str=",") -> tuple:
    """ Load a single .csv file or all files withing a directory.

    Args:
        source(Path): Path for a single file or directory with files.
        delimiter(str, optional): Separator for columns in the csv's. Default to ","
    Returns:
        tuple: All dataframes loaded from the given source path.
    """
    if source.is_file():
        logger.info("Reading csv file %s", source)
        file = open(source, "r")
        data = list()
        data.append(file)
        return tuple(data)

    
    logger.info("Reading all files within the directory: %s", source)
    data = list()
    for i in source.iterdir():
        file = open(i, "r")
        data.append(file)

    return tuple(data)


def save_to_json_file(csvs: tuple, output_path: Path, prefix: str = None, delimiter: str=","):
    """ Save dataframes to disk

    Args:
        csvs (tuple): Tuple with dataframes that will be converted.
        output_path (Path): Path where to save the .json files.
        prefix (str, optional): Name to prepend to files.
        if nothing is given, it will use 'file_'. Defaults to None.
    """
    i = 0
    while i < len(csvs):
        file_name = f"{prefix}_{i}.json"
        output = output_path.joinpath(file_name)
        logger.info("Saving file as %s", output)

        header = csvs[i].readline().rstrip("\n").split(delimiter)
        dic_list = []
        
        file = open(file_name, "w")
        for line in csvs[i]:
            dictionary = {}
            str_line = line.rstrip("\n").split(delimiter)
            for j in range(len(str_line)):
                if (str_line[j].isdigit()):
                    dictionary[header[j]] = int(str_line[j])
                elif (str_line[j] == ""):
                    dictionary[header[j]] = None
                else:
                    try:
                        float(str_line[j])
                        dictionary[header[j]] = float(str_line[j])
                    except ValueError:
                        dictionary[header[j]] = str_line[j]

            dic_list.append(dictionary)

        file.write(json.dumps(dic_list, indent=4))
        file.close()

        i += 1
