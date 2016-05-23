#!/bin/bash

file=$1
curl http://localhost:8983/solr/globus/update?commit=true -H 'Content-type:application/json' --data @${file}
