#!/bin/bash
awslocal s3 mb s3://db-bucket

awslocal s3 cp /tmp/code/athletes.parquet s3://db-bucket/athletes/athletes.parquet