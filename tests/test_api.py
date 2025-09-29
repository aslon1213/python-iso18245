import pytest
import os 
import sys 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import src.iso18245_uz as m


def test_validate_mcc_valid():
    assert m.validate_mcc("742") == 742


def test_validate_mcc_invalid_high():
    with pytest.raises(m.InvalidMCC):
        m.validate_mcc("10000")


def test_get_mcc_range_non_reserved_742():
    r = m.get_mcc_range("742")
    assert r.start == "700"
    assert r.end == "999"
    assert r.description == "Agricultural services"
    assert r.reserved is False


def test_get_mcc_range_reserved_0500():
    r = m.get_mcc_range("0500")
    assert r.start == "0"
    assert r.end == "699"
    assert r.description == "Reserved"
    assert r.reserved is True


def test_get_mcc_non_reserved_details_742():
    mcc = m.get_mcc("742")
    assert mcc.mcc == "742"
    assert mcc.range.reserved is False
    # From iso18245_official_list_translated.csv
    assert mcc.iso_description == "Veterinary services"
    # From stripe_list_translated.csv
    assert mcc.stripe_code == "veterinary_services"


def test_get_mcc_reserved_details_3000():
    mcc = m.get_mcc("3000")
    assert mcc.mcc == "3000"
    assert mcc.range.reserved is True
    # Reserved range should not set ISO description
    assert mcc.iso_description == ""
    # From visa_list_translated.csv
    assert mcc.visa_description == "UNITED AIRLINES"
    assert mcc.visa_req_clearing_name == "UNITED AIR"
    # From mastercard_list_translated.csv
    assert mcc.mastercard_abbreviated_airline_name == "UNITED"


def test_get_mcc_not_found_0500():
    with pytest.raises(m.MCCNotFound):
        m.get_mcc("0500")


def test_get_all_mccs_in_range_single_742():
    items = m.get_all_mccs_in_range("742", "742")
    assert len(items) == 1
    assert items[0].mcc == "742"


def test_get_all_mccs_dict_contains_sample_742():
    items = m.get_all_mccs_dict()
    sample = next(x for x in items if x["mcc"] == "742")
    assert sample["mcc_range_start"] == "700"
    assert sample["mcc_range_end"] == "999"
    assert sample["mcc_range_reserved_flag"] is False
    assert sample["iso_description"] == "Veterinary services"
    assert sample["stripe_code"] == "veterinary_services"


