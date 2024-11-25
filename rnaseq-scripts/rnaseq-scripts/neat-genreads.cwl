#!/usr/bin/env cwl-runner

cwlVersion: v1.2

requirements:
  - class: DockerRequirement
    dockerPull: neat
  - class: InlineJavascriptRequirement
  - class: ResourceRequirement
    coresMin: 1
    coresMax: 1
    ramMin: 1000
    ramMax: 1000
    tmpdirMin: 1
    tmpdirMax: 1
    outdirMin: 1
    outdirMax: 1
  - class: ShellCommandRequirement


class: CommandLineTool

inputs:
  - id: reference
    type: File
    inputBinding:
      prefix: -r
    secondaryFiles:
      - .fai

  - id: readlength
    type: int
    inputBinding:
      prefix: -R

  - id: output_prefix
    type: string
    inputBinding:
      prefix: -o

  - id: coverage
    type: ["null", int]
    inputBinding:
      prefix: -c

  - id: error_model
    type: ["null", string]
    inputBinding:
      prefix: -e

  - id: error_rate
    type: ["null", double]
    inputBinding:
      prefix: -E

  - id: ploidy
    type: ["null", int]
    inputBinding:
      prefix: -p

  - id: target_bed
    type: ["null", File]
    inputBinding:
      prefix: -tr

  - id: discard_regions_bed
    type: ["null", File]
    inputBinding:
      prefix: -dr

  - id: off_target_coverage_scalar
    type: ["null", double]
    inputBinding:
      prefix: -to

  - id: model_p
    type: ["null", string]
    inputBinding:
      prefix: -m

  - id: mut_rate
    type: ["null", double]
    inputBinding:
      prefix: -M

  - id: mut_rates_bed
    type: ["null", File]
    inputBinding:
      prefix: -Mb

  - id: min_qual_score
    type: ["null", int]
    inputBinding:
      prefix: -N

  - id: vcf_file
    type: ["null", File]
    inputBinding:
      prefix: -v

  - id: pe_length_std
    type: ["null", string]
    inputBinding:
      prefix: --pe
      shellQuote: false

  - id: pe_model
    type: ["null", string]
    inputBinding:
      prefix: --pe-model

  - id: gc_model
    type: ["null", string]
    inputBinding:
      prefix: --gc-model

  - id: bam
    type: ["null", boolean]
    inputBinding:
      prefix: --bam

  - id: vcf
    type: ["null", boolean]
    inputBinding:
      prefix: --vcf

  - id: fa
    type: ["null", boolean]
    inputBinding:
      prefix: --fa

  - id: rng
    type: ["null", long]
    inputBinding:
      prefix: --rng

  - id: no_fastq
    type: ["null", boolean]
    inputBinding:
      prefix: --no-fastq

  - id: discard_offtarget
    type: ["null", boolean]
    inputBinding:
      prefix: --discard-offtarget

  - id: force_coverage
    type: ["null", boolean]
    inputBinding:
      prefix: --force-coverage

  - id: rescale_qual
    type: ["null", boolean]
    inputBinding:
      prefix: --rescale-qual

  - id: debug
    type: ["null", boolean]
    inputBinding:
      prefix: -d

outputs:
  - id: fastq
    type:
      type: array
      items: File
    outputBinding:
      glob: '*.fq.gz'

  - id: bam
    type: File
    outputBinding:
      glob: $(inputs.output_prefix)_golden.bam

  - id: vcf
    type: File
    outputBinding:
      glob: $(inputs.output_prefix)_golden.vcf.gz

baseCommand: [python3, /neat-genreads/gen_reads.py]
