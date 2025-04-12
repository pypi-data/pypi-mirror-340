#!/bin/bash
# usage: ./run_ingest.sh <venv-name> <datahub-version> <plugins-required> <tmp-dir> <recipe_file> <report_file>

set -euo pipefail
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR" || exit

source ingestion_common.sh

venv_name="$1"
datahub_version="$2"
plugins="$3"
tmp_dir="$4"
recipe_file="$5"
report_file="$6"
debug_mode="$7"

create_venv $venv_name $datahub_version $plugins $tmp_dir

# Activate the newly created venv and install custom plugin
source "${tmp_dir}/venv-${venv_name}/bin/activate"
pip install /plugins/json-ingester/dist/json_ingester-0.1.0-py3-none-any.whl

if (datahub ingest run --help | grep -q report-to); then
  echo "This version of datahub supports report-to functionality"
  rm -f "$report_file"
  report_option="--report-to ${report_file}"
else
  report_option=""
fi

if [ "$debug_mode" == "true" ]; then 
  debug_option="--debug"
else
  debug_option=""
fi;

# Execute DataHub recipe, based on the recipe id.
set -x
exec datahub ${debug_option} ingest run -c "${recipe_file}" ${report_option}
