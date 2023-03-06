#! /bin/sh

# Backup existing chromedriver
mv chromedriver chromedriver.backup

# Download from repository
wget https://chromedriver.storage.googleapis.com/110.0.5481.77/chromedriver_linux64.zip

# Unzip the archive
unzip chromedriver_linux64.zip

# Remove the archive
rm chromedriver_linux64.zip

# Remove the LICENSE file
rm LICENSE.chromedriver
