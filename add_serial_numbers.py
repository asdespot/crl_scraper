import asn1crypto.crl
import os
import asn1crypto.pem


def read_crl_serial_numbers(cert_path):
    all_serial_numbers = []

    for crl_cert in os.listdir(cert_path):
        if crl_cert.endswith(".crl"):
            crl_file_path = os.path.join(cert_path, crl_cert)
            if os.path.isfile(crl_file_path):
                with open(crl_file_path, 'rb') as crl_file:
                    crl_data = crl_file.read()
                    try:
                        # Try to load CRL in DER format
                        crl = asn1crypto.crl.CertificateList.load(crl_data)
                        issuer = crl['tbs_cert_list']['issuer'].human_friendly
                        for revoked_cert in crl['tbs_cert_list']['revoked_certificates']:
                            serial_number = str(revoked_cert['user_certificate'].native)
                            all_serial_numbers.append((serial_number, issuer, crl_cert))
                    except Exception as e:
                        print(f"Failed to load CRL in DER format for {crl_cert}: {e}")

                        # Try to handle PEM format CRLs
                        try:
                            if asn1crypto.pem.detect(crl_data):
                                _, _, crl_data = asn1crypto.pem.unarmor(crl_data)
                                crl = asn1crypto.crl.CertificateList.load(crl_data)
                                issuer = crl['tbs_cert_list']['issuer'].human_friendly
                                for revoked_cert in crl['tbs_cert_list']['revoked_certificates']:
                                    serial_number = str(revoked_cert['user_certificate'].native)
                                    all_serial_numbers.append((serial_number, issuer, crl_cert))
                        except Exception as e:
                            print(f"Failed to handle PEM CRL for {crl_cert}: {e}")

    return all_serial_numbers


if __name__ == '__main__':
    certs_path = "path_to_crl_files"
    serial_numbers = read_crl_serial_numbers(certs_path)
    for serial in serial_numbers:
        print(serial)