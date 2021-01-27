date=$(date +%Y)
echo -e "======================\ndiscogsScreener © $date\n======================\n"


# install prology with pip3 (python3)
echo installing prology ...
pip3 install git+https://github.com/B0-B/prology.git#egg=prology
echo done .

# install discogs client
echo installing dicogs client ...
pip3 install git+https://github.com/joalla/discogs_client.git#egg=discogs_client
echo done .