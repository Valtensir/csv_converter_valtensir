# A  CSV <> JSON converter

A CSV to JSON and JSON to CSV converter.

## Introduction

A project to learning porpuses. 

## What this project can do

1 - Read a csv file or a folder with csv's and convert them to JSON.

2 - Read a json file or a folder with json's and convert them to CSV.

This project is a program running on terminal, preferably install with pipx:

```bash
pipx install csv_converter_valtensir
```

## Help
```bash
Usage: csv_converter [OPTIONS]

Options:
  -c, --convert TEXT    Format you want to convert. cc -> Convert CSV to JSON;
                        cj -> Convert JSON to CSV.
  -i, --input TEXT      Path where to find the files to convert.
  -o, --output TEXT     Path where the converted files will be saved.
  -d, --delimiter TEXT  Separator used to split the files.
  -p, --prefix TEXT     Prefix used to prepend to the name of the converted
                        file saved on disk.The suffix will be a number
                        starting from 0. ge: file_0
  --help                Show this message and exit.

```