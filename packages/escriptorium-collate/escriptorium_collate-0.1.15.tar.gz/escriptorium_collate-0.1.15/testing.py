import json
import os

from escriptorium_connector import EscriptoriumConnector

from escriptorium_collate import transcription_layers
from escriptorium_collate.collate import (
    CollatexArgs,
    Witness,
    collate,
    get_collatex_input,
    get_collatex_output,
)

url = "https://preprod-escriptorium.openiti.org/"
username = "oeshera"
password = "HTc9RbapK4F9N2"

escr = EscriptoriumConnector(url, username, password)

collatex_args = CollatexArgs()

witnesses = [
    Witness(
        doc_pk=74,
        siglum="A",
        diplomatic_transcription_name="manual",
        normalized_transcription_name="New Layer",
    ),
    Witness(
        doc_pk=75,
        siglum="B",
        diplomatic_transcription_name="manual",
        normalized_transcription_name="manual",
    ),
    # Witness(
    #     doc_pk=76,
    #     siglum="C",
    #     diplomatic_transcription_name="manual",
    #     normalized_transcription_name="manual",
    # ),
    # Witness(
    #     doc_pk=77,
    #     siglum="D",
    #     diplomatic_transcription_name="manual",
    #     normalized_transcription_name="manual",
    # ),
    # Witness(
    #     doc_pk=78,
    #     siglum="E",
    #     diplomatic_transcription_name="manual",
    #     normalized_transcription_name="manual",
    # ),
    # Witness(
    #     doc_pk=79,
    #     siglum="F",
    #     diplomatic_transcription_name="manual",
    #     normalized_transcription_name="manual",
    # ),
    # Witness(
    #     doc_pk=80,
    #     siglum="G",
    #     diplomatic_transcription_name="manual",
    #     normalized_transcription_name="manual",
    # ),
    # Witness(
    #     doc_pk=81,
    #     siglum="H",
    #     diplomatic_transcription_name="manual",
    #     normalized_transcription_name="manual",
    # ),
]

# transcription_layers.create(escr=escr, doc_pk=74, layer_name="New Layer")

collatex_input = get_collatex_input(escr=escr, witnesses=witnesses, collatex_args=CollatexArgs())
with open('/my-dir/collatex_input.json', 'w', encoding='utf-8') as f:
    json.dump(collatex_input, f, ensure_ascii=False, indent=4)


collatex_output = get_collatex_output(collatex_args=CollatexArgs(input='/my-dir/collatex_input.json'))
with open('/my-dir/collatex_output.json', 'w', encoding='utf-8') as f:
    json.dump(collatex_output, f, ensure_ascii=False, indent=4)

collatex_output = collate(escr=escr, witnesses=witnesses, collatex_args=collatex_args)


for row_index, row in enumerate(collatex_output['table']):
    for cell_index, cell in enumerate(row):
        for token_index, token in enumerate(cell):
            for key, value in token.items():
                if key in ('n', 't') and value == " ":
                    token[key] = ""


doc_pk = 83
parts = escr.get_document_parts(doc_pk=doc_pk).results
for part in parts:
    lines = escr.get_document_part_lines(doc_pk=doc_pk, part_pk=part.pk).results
    for line in lines:
        normalized_line = escr.get_document_part_line_transcription_by_transcription(
            doc_pk=doc_pk,
            part_pk=part.pk,
            line_pk=line.pk,
            transcription_pk=427,
        )
        diplomatic_line = escr.get_document_part_line_transcription_by_transcription(
            doc_pk=doc_pk,
            part_pk=part.pk,
            line_pk=line.pk,
            transcription_pk=147,
        )
        break


# poetry publish --skip-existing
# poetry build