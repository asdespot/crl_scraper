import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os
import uuid

root_urls = [
    {"name": "halcom", "url": "https://domina.halcom.rs/crls/?C=N;O=A", "scrape": True,
     "download_link": "https://domina.halcom.rs/crls/"},
    {"name": "halcom", "url": "https://domina.halcom.rs/crls/binary/", "scrape": True,
     "download_link": "https://domina.halcom.rs/crls/binary/"},
    {"name": "halcom", "url": "https://domina.halcom.rs/crls/kobb/", "scrape": True,
     "download_link": "https://domina.halcom.rs/crls/kobb/"},
    {"name": "halcom", "url": "https://domina.halcom.rs/crls/kobb/binary/", "scrape": True,
     "download_link": "https://domina.halcom.rs/crls/kobb/binary/"},
    {"name": "halcom", "url": "https://domina.halcom.rs/crls/nlb/", "scrape": True,
     "download_link": "https://domina.halcom.rs/crls/nlb/"},
    {"name": "halcom", "url": "https://domina.halcom.rs/crls/Halcom_BG_CA.crl", "scrape": False,
     "download_link": ""},
    {"name": "pks", "url": "http://v3.pksca.rs/crl/PKSCATSA.crl", "scrape": False,
     "download_link": ""},
    {"name": "pks", "url": "http://v3.pksca.rs/crl/PKSCARoot.crl", "scrape": False,
     "download_link": ""},
    {"name": "pks", "url": "http://v3.pksca.rs/crl/PKSCAClass1.crl", "scrape": False,
     "download_link": ""},
    {"name": "pks", "url": "http://v3.pksca.rs/crl/PKSCACloud.crl", "scrape": False,
     "download_link": ""},
    {"name": "halcom", "url": "https://domina.halcom.rs/crls/Halcom_BG_Root_CA.crl", "scrape": False,
     "download_link": ""},
    {"name": "halcom", "url": "https://domina.halcom.rs/crls/Halcom_BG_CA_PL_e-signature.crl", "scrape": False,
     "download_link": ""},
    {"name": "halcom", "url": "https://domina.halcom.rs/crls/Halcom_BG_CA_FL_e-signature.crl", "scrape": False,
     "download_link": ""},
    {"name": "halcom", "url": "https://domina.halcom.rs/crls/Halcom_BG_CA_PL.crl", "scrape": False,
     "download_link": ""},
    {"name": "halcom", "url": "https://domina.halcom.rs/crls/Halcom_BG_CA_FL.crl", "scrape": False,
     "download_link": ""},
    {"name": "halcom", "url": "https://domina.halcom.rs/crls/Halcom_BG_CA_PL3.crl", "scrape": False,
     "download_link": ""},
    {"name": "halcom", "url": "https://domina.halcom.rs/crls/Halcom_BG_CA_FL3.crl", "scrape": False,
     "download_link": ""},

    {"name": "halcom si", "url": "http://domina.halcom.si/crls/halcom_root_certificate_authority.crl", "scrape": False,
     "download_link": ""},

    {"name": "halcom si", "url": "http://domina.halcom.si/crls/halcom_ca_po_e-signature_1.crl", "scrape": False,
     "download_link": ""},

    {"name": "halcom si", "url": "http://domina.halcom.si/crls/halcom_ca_po.crl", "scrape": False,
     "download_link": ""},

    {"name": "halcom si", "url": "https://www.halcom.com/sl_en/halcom-ca-en/list-of-revoked-certificates/",
     "scrape": True, "download_link": ""},

    {"name": "halcom rs", "url": "https://www.halcom.com/rs/halcom-ca-3/opozvani-sertifikati/", "scrape": True,
     "download_link": ""},

    {"name": "mup", "url": "http://crl.mup.gov.rs/CRL.html", "scrape": True, "download_link": "http://crl.mup.gov.rs/"},
    {"name": "posta", "url": "http://repository.ca.posta.rs/crl/PostaSrbijeCA1.crl", "scrape": False,
     "download_link": ""},
    {"name": "posta", "url": "http://sertifikati.ca.posta.rs/crl/PostaCA1.crl", "scrape": False, "download_link": ""},

    {"name": "eid", "url": "https://cloud.eid.gov.rs/ca/eidroot.crl", "scrape": False, "download_link": ""},
    {"name": "eid", "url": "https://cloud.eid.gov.rs/ca/eidsign.crl", "scrape": False, "download_link": ""},
    {"name": "eid", "url": "https://cloud.eid.gov.rs/ca/eidusr.crl", "scrape": False, "download_link": ""},
]

# root_urls = [ ]

sub_sites = ["binary/", "kobb/", "	nlb/", "text/"]

script_dir = os.path.dirname(os.path.abspath(__file__))
download_directory = os.path.join(script_dir, "crl")

cert_list = []


def get_unique_file_name(file_name):
    base_name, extension = os.path.splitext(file_name)
    random_suffix = uuid.uuid4().hex[:8]
    file_name = f"{base_name}-{random_suffix}{extension}"
    return file_name


def get_certificate_name(url):
    parsed_url = urlparse(url)
    certificate_name = parsed_url.path.split('/')[-1]
    return certificate_name.lower()


def download_file(download_url, link=None):
    folder_list = []
    try:
        # Ensure the download directory exists
        if not os.path.exists(download_directory):
            os.makedirs(download_directory)

        full_url = ""
        if link is not None:
            full_url = urljoin(download_url, link)
        else:
            full_url = download_url

        link_response = requests.get(full_url)
        file_name = get_certificate_name(full_url)

        if file_name in cert_list:
            file_name = get_unique_file_name(file_name)

        if link_response.status_code == 200:
            with open(os.path.join(download_directory, file_name), 'wb') as file:
                file.write(link_response.content)
                print(f"Downloaded: {file_name}")
                cert_list.append(file_name.lower())

            for file_crl in os.listdir(download_directory):
                if file_crl.endswith(".crl"):
                    folder_list.append(file_crl)
        else:
            print(f"Failed to download {full_url}: HTTP Status Code {link_response.status_code}")

    except requests.exceptions.RequestException as req_err:
        print(f"Network error occurred while downloading {full_url}: {req_err}")
    except FileNotFoundError as fnf_err:
        print(f"File not found error: {fnf_err}")
    except IOError as io_err:
        print(f"IO error occurred: {io_err}")
    except Exception as e:
        print(f"An error occurred: {e}")


def scrape_page_links(url):
    links = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            for link in soup.find_all('a'):
                links.append(link.get('href'))
        else:
            print(f"Failed to scrape {url}: HTTP Status Code {response.status_code}")
    except requests.exceptions.RequestException as req_err:
        print(f"Network error occurred while scraping {url}: {req_err}")
    except Exception as e:
        print(f"An error occurred while scraping {url}: {e}")

    return links


def main():
    for value in root_urls:
        name = value.get("name")
        url = value.get("url")
        scrape = value.get("scrape")
        download_url = value.get("download_link")

        if scrape:
            href_links = scrape_page_links(url)

            try:
                for link in href_links:
                    if link.endswith(".crl"):
                        download_file(download_url, link)

            except Exception as e:
                print(f"An error occurred while processing {url}: {e}")

        else:
            try:
                download_file(url, link=None)
            except Exception as e:
                print(f"An error occurred while downloading from {url}: {e}")


if __name__ == '__main__':
    main()

