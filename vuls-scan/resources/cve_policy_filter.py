"""
Implement policy based on
https://wiki.openstack.org/wiki/StarlingX/Security/CVE_Support_Policy

Document as pydoc -w cve_policy_filter

Vulscan generates two files, please save them as:

VULS scan report full text <date> ->  cves_report_full.txt
VULS scan report format list <date> -> cves_report_list.txt

Run this script as  python cve_policy_filter.py

"""
import os
import sys

def get_cvss_position(lines):
        for line in lines:
            line = line.strip()
            if "CVE-ID" in line and "CVSS" in line:
                elements = (line.split("|"))
                count = 0
                for element in elements:
                    if "CVSS"  in element.strip():
                        return count
                    count +=1

def get_cvss(cve_id,filename):
    """
    Get the CVSS score of a CVE
    CVSS, Common Vulnerability Scoring System, is a vulnerability
    scoring system designed to provide an open and standardized method for
    rating IT vulnerabilities.
    :param filename: The name of the file with the CVEs metadata
    :param cve_id: ID of the CVE is necesary to get the CVSS score
    :return: return the CVSS score
    """
    with open(filename,'r') as fh:
        lines = fh.readlines()
        pos = get_cvss_position(lines)
        for line in lines:
            line = line.strip()
            if "CVE" in line and not "CVE-ID" in line:
                if cve_id in (line.split("|")[1]):
                    cvss = (line.split("|")[pos])
                    print(cve_id + "    " + cvss)
                    return cvss

def get_cves_status(cve_id,filename):
    """
    Get the CVEs status : fixed/unfixed
    :return cve_status
    """
    cve_ids = []
    with open(filename,'r') as fh:
        lines = fh.readlines()
        for line in lines:
            if "CVE" in line and not "CVE-ID" in line:
                if cve_id in line:
                    cve_status = line.strip().split("|")[2].strip()
                    return cve_status

def get_cves_id(filename):
    """
    Get the CVEs ids from the vulscan document
    :param filename: The name of the file with the CVEs metadata
    :return: return the CVE ids as array
    """
    cve_ids = []
    with open(filename,'r') as fh:
        lines = fh.readlines()
        for line in lines:
            if "CVE" in line and not "CVE-ID" in line:
                cve_id = (line.strip().split("|")[1])
                if cve_id not in cve_ids:
                    cve_ids.append(cve_id.strip())
    return cve_ids

def get_base_vector(cve_id,filename):
    """
    Get Base Metrics vector:
    Attack-vector: Context by which vulnerability exploitation is possible.
    Attack-complexity: Conditions that must exist in order to exploit
    Authentication: Num of times that attacker must authenticate to exploit
    Availability-impact: Impact on the availability of the target system.
    return: Attack-vector/ Access-complexity/Authentication/Availability-impact
    """
    with open(filename,'r') as fh:
        vector = None
        av = None
        ac = None
        au = None
        ai = None
        lines = fh.readlines()
        count = 0
        cveid_position = 0
        for line in lines:
            count = count + 1
            if cve_id in line and ("UNFIXED" in line or "FIXED" in line):
                cveid_position = count
            if "nvd" in line and "Au" in line and count < (cveid_position + 10):
                vector = line.split("|")[2].strip()
                break
        if vector:
            for element in vector.split("/"):
                if "AV:" in element:
                    av = element.split(":")[1]
                if "AC:" in element:
                    ac = element.split(":")[1]
                if "Au:" in element:
                    au = element.split(":")[1]
                if "A:" in element:
                    ai = element.split(":")[1]
        return av,ac,au,ai

if __name__ == '__main__':

    cves_valid = []

    cves_report_full_file = "cves_report_full.txt"
    cves_report_list_file = "cves_report_list.txt"

    if not os.path.isfile(cves_report_list_file) or \
    not os.path.isfile(cves_report_full_file):
        print("ERROR: cves_report_full.txt and \
        cves_report_list.txt must exist")
        sys.exit(-1)

    cve_ids = get_cves_id(cves_report_list_file)

    for cve_id in cve_ids:
        cve = {}

        cvss = float(get_cvss(cve_id,cves_report_list_file))
        av,ac,au,ai = get_base_vector(cve_id,cves_report_full_file)
        cve_status = get_cves_status(cve_id,cves_report_list_file)
        """
        Following rules from:
        https://wiki.openstack.org/wiki/StarlingX/Security/CVE_Support_Policy
        """

        if  cvss >= 7.0\
        and av == "N"\
        and ac == "L"\
        and (au == "N" or au == "S")\
        and (ai == "P" or ai == "C")\
        and cve_status == "fixed":
            cve["id"] = cve_id
            cve["cvss"] = cvss
            cve["av"] = av
            cve["ac"] = ac
            cve["au"] = au
            cve["ai"] = ai
            cve["status"] = cve_status
            cves_valid.append(cve)

    for cve in cves_valid:
        print(cve)

