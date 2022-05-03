#!/bin/bash

while read url; do
    wget --continue $url
done < urls.txt