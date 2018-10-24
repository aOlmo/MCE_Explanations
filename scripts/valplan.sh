#!/usr/bin/env bash
VAL_PATH=$(locate VAL/validate | head -n 1)
${VAL_PATH} $1 $2 $3
