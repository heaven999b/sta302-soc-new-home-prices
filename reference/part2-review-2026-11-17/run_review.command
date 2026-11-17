#!/bin/bash
set -eu
cd -- "$(dirname -- "$0")"
if command -v Rscript >/dev/null 2>&1; then
  REVIEW_R=$(command -v Rscript)
elif [ -x /opt/anaconda3/envs/sta302r/bin/Rscript ]; then
  REVIEW_R=/opt/anaconda3/envs/sta302r/bin/Rscript
  export PATH="/opt/anaconda3/envs/sta302r/bin:$PATH"
else
  echo 'Rscript is not installed. Install R and the packages listed in README_START_HERE.txt.'
  exit 1
fi
export LC_ALL=en_US.UTF-8
"$REVIEW_R" -e 'rmarkdown::render("Part2_Analysis_review.Rmd")'
echo 'Rendered Part2_Analysis_review.html. Test evaluation remained disabled.'
