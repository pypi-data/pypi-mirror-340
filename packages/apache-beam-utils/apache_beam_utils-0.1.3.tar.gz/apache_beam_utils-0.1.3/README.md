# apache_beam_utils

## Status

[![PyPI version](https://badge.fury.io/py/apache-beam-utils.svg)](https://badge.fury.io/py/apache-beam-utils) [![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/MIT) 

## Overview:
This repository contains a carefully extracted subset of utility modules from the Apache Beam Python SDK, focusing primarily on apache_beam.utils.python_callable.py and its necessary companions.

## Problem Addressed:
The Apache Beam SDK is a powerful framework for building data processing pipelines, but it constitutes a large and complex dependency. Developers may find certain utility functions within Beam, such as those provided by python_callable.py, highly useful in contexts outside of full-scale Beam pipelines. However, depending on the entire apache-beam package solely for these utilities introduces significant overhead and potential dependency conflicts.

## Solution:
This project provides these specific Beam utilities in an isolated, minimal package. By extracting python_callable.py and its immediate dependencies from the main Beam codebase, we offer developers the ability to leverage this functionality without incurring the cost of installing the full Beam SDK. This promotes modularity and helps maintain leaner dependency trees in projects that benefit from this specific utility.

## Licensing:
The code herein is sourced from the Apache Beam project and is made available under the original Apache License 2.0. Please ensure compliance with the terms of this license. This project is not affiliated with or endorsed by the Apache Software Foundation.